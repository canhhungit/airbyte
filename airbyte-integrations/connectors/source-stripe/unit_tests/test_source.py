#
# Copyright (c) 2023 Airbyte, Inc., all rights reserved.
#
import datetime
import logging
from contextlib import nullcontext as does_not_raise
from unittest.mock import patch

import freezegun
import pytest
import source_stripe
import stripe
from airbyte_cdk.sources.streams.call_rate import CachedLimiterSession, LimiterSession
from airbyte_cdk.sources.streams.http import HttpStream
from airbyte_cdk.utils import AirbyteTracedException
from source_stripe import SourceStripe

logger = logging.getLogger("airbyte")


def _a_valid_config():
    return {"account_id": 1, "client_secret": "secret"}


@patch.object(source_stripe.source, "stripe")
def test_source_check_connection_ok(mocked_client, config):
    assert SourceStripe().check_connection(logger, config=config) == (True, None)


def test_streams_are_unique(config):
    stream_names = [s.name for s in SourceStripe().streams(config=config)]
    assert len(stream_names) == len(set(stream_names)) == 46


@pytest.mark.parametrize(
    "input_config, expected_error_msg",
    (
        ({"lookback_window_days": "month"}, "Invalid lookback window month. Please use only positive integer values or 0."),
        ({"start_date": "January First, 2022"}, "Invalid start date January First, 2022. Please use YYYY-MM-DDTHH:MM:SSZ format."),
        ({"slice_range": -10}, "Invalid slice range value -10. Please use positive integer values only."),
        (_a_valid_config(), None),
    ),
)
@patch.object(source_stripe.source.stripe, "Account")
def test_config_validation(mocked_client, input_config, expected_error_msg):
    context = pytest.raises(AirbyteTracedException, match=expected_error_msg) if expected_error_msg else does_not_raise()
    with context:
        SourceStripe().check_connection(logger, config=input_config)


@pytest.mark.parametrize(
    "exception",
    (
        stripe.error.AuthenticationError,
        stripe.error.PermissionError,
    ),
)
@patch.object(source_stripe.source.stripe, "Account")
def test_given_stripe_error_when_check_connection_then_connection_not_available(mocked_client, exception):
    mocked_client.retrieve.side_effect = exception
    is_available, _ = SourceStripe().check_connection(logger, config=_a_valid_config())
    assert not is_available


@pytest.mark.parametrize(
    "input_config, default_call_limit",
    (
        ({"account_id": 1, "client_secret": "secret"}, 100),
        ({"account_id": 1, "client_secret": "secret", "call_rate_limit": 10}, 10),
        ({"account_id": 1, "client_secret": "secret", "call_rate_limit": 110}, 100),
        ({"account_id": 1, "client_secret": "sk_test_some_secret"}, 25),
        ({"account_id": 1, "client_secret": "sk_test_some_secret", "call_rate_limit": 10}, 10),
        ({"account_id": 1, "client_secret": "sk_test_some_secret", "call_rate_limit": 30}, 25),
    ),
)
@freezegun.freeze_time("2021-01-01")
def test_call_budget_creation(mocker, input_config, default_call_limit):
    """Test that call_budget was created with specific config i.e., that first policy has specific matchers."""

    fixed_window_mock = mocker.patch("source_stripe.source.FixedWindowCallRatePolicy")
    matcher_mock = mocker.patch("source_stripe.source.HttpRequestMatcher")
    source = SourceStripe()

    source.get_api_call_budget(input_config)

    fixed_window_mock.assert_has_calls(
        calls=[
            mocker.call(
                matchers=[mocker.ANY, mocker.ANY],
                call_limit=20,
                next_reset_ts=datetime.datetime.now(),
                period=datetime.timedelta(seconds=1),
            ),
            mocker.call(
                matchers=[],
                call_limit=default_call_limit,
                next_reset_ts=datetime.datetime.now(),
                period=datetime.timedelta(seconds=1),
            ),
        ],
    )

    matcher_mock.assert_has_calls(
        calls=[
            mocker.call(url="https://api.stripe.com/v1/files"),
            mocker.call(url="https://api.stripe.com/v1/file_links"),
        ]
    )


def test_call_budget_passed_to_every_stream(mocker):
    """Test that each stream has call_budget passed and creates a proper session"""

    prod_config = {"account_id": 1, "client_secret": "secret"}
    source = SourceStripe()
    get_api_call_budget_mock = mocker.patch.object(source, "get_api_call_budget")

    streams = source.streams(prod_config)

    assert streams
    get_api_call_budget_mock.assert_called_once()

    for stream in streams:
        assert isinstance(stream, HttpStream)
        session = stream.request_session()
        assert isinstance(session, (CachedLimiterSession, LimiterSession))
        assert session._api_budget == get_api_call_budget_mock.return_value
