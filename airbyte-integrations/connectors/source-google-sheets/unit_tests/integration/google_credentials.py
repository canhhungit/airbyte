# Copyright (c) 2024 Airbyte, Inc., all rights reserved.

# todo check if we can make fake private_key it pass RSA validation, then we wouldn't need to mock Credentials classes
service_account_info = (
    "{\n"
    "  \"type\": \"service_account\",\n"
    "  \"project_id\": \"test-project\",\n"
    "  \"private_key_id\": \"fake-private-key-id\",\n"
    "  \"private_key\": \"-----BEGIN PRIVATE KEY-----\\n"
    "MIIEpAIBAAKCAQEAmPLhTvRiazktIFs/huGm+7Yvl1NH2OBJDwnb2rc6bXvIS9to\\n"
    "n/+ImDziOeEQDa2L1gkwmkxxjDILxbnu/M2CaeH5CDCB0o4s77bzW0ndPswsA0HZ\\n"
    "EOVydooBltBgP0reaswFPrTvF9Z9xTRaYQa0wUIwm7AlV6lhZqXrM//D0z39NpTy\\n"
    "ADvh6LgnuU/hUQGaQgPtueTEwxKlfQeoMASJhTY0gARJ+gdlloMCQBl3DbzXGxBR\\n"
    "PdvsQ4f2y9KxIT+aor0MgxcJLN22dn0MT7THZp+p2jv2OGgULMIifMbvvlrqtEkR\\n"
    "xJNF3SzYo8kE8ogn+Vs59T0p8ei8agP7ea892wIDAQABAoIBAB8RNrLS8SrWclQg\\n"
    "NMcxDroSR5h1UiK7bBuh5QaIMVYLzqOZ7aaSQSyrMUiQbrJYjg7rzvOIk4fmon2H\\n"
    "RwQSumrHe84uDDC4sGgAwW3JkycuUcJXnb/Q2284mRoJOYOhsYv/5RDXr7kn2GQ2\\n"
    "PiV3N0AKMdVt8ifcP+yZxyzIxv4hSOqe6y99081EcjWqf59VQ9zDf2HH/hpWQSlE\\n"
    "qiU0Ie1p6SqgLK6thiKZZKBctV8N86oww1pW68+Fj8ath7h7Yyjqv+IrNHOlafX7\\n"
    "MHyF0szUPHr3uy5nrHRzS5IEBZziRRg+n6uMTdjVX53z4WG6Sj29bcoRodXz5MHO\\n"
    "Q3jr4AECgYEAxnKBAZWSEkWc9qmK+KEu0UclmvabQSB7zcTuyQoAK6ZulZeS1l9J\\n"
    "Spt/09jne49UOrx4eUerLF9EMAQjGsGKRS2WOuhVEXIzhx0x8hNvHgt/YZrjcutM\\n"
    "7oPnV+Bi8heulZHu1PcxsZwXqI1a08DqJOlTQFGVFSt7k/ODIJE3xm8CgYEAxU5j\\n"
    "hRAHSUUZ+I83k5MdL2cI2+RgSSD3i2uta+G+E2EDfoNXKD3uUg4ZMjcraR0dLIVG\\n"
    "97+IBBNQtotuFGl+pf1/4Vso6tQDdjTi+mUS58Q4t/R+2y7ltR5l3jN5sLXn/J/R\\n"
    "xxF1ZgBny2iEW9ruZa1sD6YhFT6fuKk26E7w1VUCgYBxwCTOgavPKXQFt71fMxUh\\n"
    "BMU7hGwN8s7EbkPpnP/oBWiR+uZCVzAtweCN0GEv5EKFwI7WBgzKTHlLhLOSnKnj\\n"
    "aXQZpB9O9sUuh7+fYSBqenCzxBLoRpQ8jANJzecpmgWK2rGqBV/IzQ6KoSwVARm1\\n"
    "usDrt1fbYKdfcVASlOsBpQKBgQCm57PaKP/w5Eqe8A/0f5tNsRxWXy9wTTn6r8DJ\\n"
    "JPJUlFmPWO2Otiz3LsPzraXESoOWWLv68gPOZsR9Vx9slv0yz2mxKhtH4sd25DAp\\n"
    "3vyKIHxWaLYzFc3tU+SaffLwIEE5e7zKaCNmgOtMr4Jf7aiDTJu/9SnBPfOBE2vG\\n"
    "QpkJ7QKBgQCaCeEnIR5wQnvrxT6N/IR9LHObQxYHilGmv+i/g9ouf8+AUoYBUitN\\n"
    "D5aUbD+gsDZZN7ARxA/18mnnNmGpHCml30caCGE88t+vT7Z7QHMeW2oqWwC29JZ0\\n"
    "sPIYH1+LzU7rCpjRzo3gApY9DbazIXPSc3Gshc1JWuykOq4Zv8GnWg==\\n"
    "-----END PRIVATE KEY-----\\n\",\n"
    "  \"client_email\": \"test-service-account@test-project.iam.gserviceaccount.com\",\n"
    "  \"client_id\": \"1234567890\",\n"
    "  \"auth_uri\": \"https://accounts.google.com/o/oauth2/auth\",\n"
    "  \"token_uri\": \"https://oauth2.googleapis.com/token\",\n"
    "  \"auth_provider_x509_cert_url\": \"https://www.googleapis.com/oauth2/v1/certs\",\n"
    "  \"client_x509_cert_url\": \"https://www.googleapis.com/robot/v1/metadata/x509/test-service-account%40test-project.iam.gserviceaccount.com\"\n"
    "}"
)

service_account_credentials = {
    "auth_type": "Service",
    "service_account_info": service_account_info,
}
