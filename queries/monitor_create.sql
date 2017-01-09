CREATE TABLE IF NOT EXISTS TABLENAME (
        table_schame VARCHAR(30),
        start_timestamp TIMESTAMP,
        transaction_id BIGINT,
        statement_id BIGINT,
        query_duration_us NUMERIC(20,5),
        resource_request_execution_ms BIGINT,
        used_memory_kb NUMERIC(20,5),
        CPU_TIME BIGINT,
        label VARCHAR(100),
	query VARCHAR(100)
        );
