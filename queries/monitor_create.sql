CREATE TABLE IF NOT EXISTS TABLENAME (
        schema_name VARCHAR(30),
        start_timestamp TIMESTAMP,
        transaction_id BIGINT,
        statement_id BIGINT,
        request_id BIGINT,
        response_ms NUMERIC(20,5),
        memory_allocated_kb NUMERIC(20,5),
        memory_used_kb NUMERIC(20,5),
        cpu_time_ms BIGINT,
        label VARCHAR(100)
        );
