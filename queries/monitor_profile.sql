SELECT 
        running_time,
        memory_allocated_bytes,
        read_from_disk_bytes,
        path_line
FROM 
	dc_snapshots.query_plan_profiles_snap qpp
WHERE 
	transaction_id = TRANSACTION_NUMBER
	--AND statement_id = STATEMENT_NUMBER;  

