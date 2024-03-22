/*
 * Copyright (c) 2023 Airbyte, Inc., all rights reserved.
 */
package io.airbyte.cdk.db.bigquery

import io.airbyte.cdk.db.ContextQueryFunction
import io.airbyte.cdk.db.Database
import org.jooq.Record
import org.jooq.Result
import org.jooq.SQLDialect
import org.jooq.exception.DataAccessException
import org.jooq.impl.DefaultDSLContext
import java.sql.SQLException

/**
 * This class is a temporary and will be removed as part of the issue @TODO #4547
 */
class TempBigQueryJoolDatabaseImpl(projectId: String?, jsonCreds: String?) : Database(null) {
    val realDatabase: BigQueryDatabase

    init {
        realDatabase = createBigQueryDatabase(projectId, jsonCreds)
    }

    @Throws(SQLException::class)
    override fun <T> query(transform: ContextQueryFunction<T>): T? {
        return transform.query(FakeDefaultDSLContext(realDatabase))
    }

    @Throws(SQLException::class)
    override fun <T> transaction(transform: ContextQueryFunction<T>): T? {
        return transform.query(FakeDefaultDSLContext(realDatabase))
    }

    private class FakeDefaultDSLContext(private val database: BigQueryDatabase) : DefaultDSLContext(null as SQLDialect?) {
        @Throws(DataAccessException::class)
        override fun fetch(sql: String): Result<Record> {
            try {
                database.execute(sql)
            } catch (e: SQLException) {
                throw DataAccessException(e.message, e)
            }
            return null
        }
    }

    companion object {
        fun createBigQueryDatabase(projectId: String?, jsonCreds: String?): BigQueryDatabase {
            return BigQueryDatabase(projectId, jsonCreds)
        }
    }
}
