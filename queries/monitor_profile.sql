SELECT 
        --transaction_id,
        --statement_id,
        running_time,
        memory_allocated_bytes,
        read_from_disk_bytes,
        path_line
FROM 
	QUERY_PLAN_PROFILES qpp
WHERE 
	transaction_id = TRANSACTION_NUMBER
	--AND statement_id = STATEMENT_NUMBER;  

