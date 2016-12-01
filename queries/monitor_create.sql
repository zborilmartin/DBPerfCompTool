CREATE TABLE IF NOT EXISTS TABLENAME (
        table_schame VARCHAR(30),
        start_timestamp TIMESTAMP,
        transaction_id BIGINT,
        statement_id BIGINT,
        query_duration_us DECIMAL(20,1),
        resource_request_execution_ms BIGINT,
        used_memory_kb DECIMAL(20,1),
        CPU_TIME INTEGER,
        label VARCHAR(100)
        );