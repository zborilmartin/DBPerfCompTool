SELECT   /*+ label(monitor_queries) */
        pu.anchor_table_schema,
        qr.start_timestamp,
        eep.transaction_id,
        eep.statement_id,
        qp.query_duration_us,
        TIMESTAMPDIFF(ms, ra.acquisition_timestamp, ra.release_timestamp) as resource_request_execution_ms,
        (ra.memory_inuse_kb - (qp.reserved_extra_memory/1024)) AS used_memory_kb,        
        SUM(eep.counter_value) as CPU_TIME,
        qp.query
FROM
        EXECUTION_ENGINE_PROFILES eep
        INNER JOIN QUERY_PROFILES qp ON eep.transaction_id = qp.transaction_id AND eep.statement_id = qp.statement_id
                        AND eep.session_id = qp.session_id AND eep.node_name = qp.node_name
        INNER JOIN QUERY_REQUESTS qr ON eep.transaction_id = qr.transaction_id AND eep.statement_id = qr.statement_id
                        AND eep.session_id = qr.session_id AND eep.node_name = qr.node_name
        INNER JOIN RESOURCE_ACQUISITIONS ra ON eep.transaction_id = ra.transaction_id AND eep.statement_id = ra.statement_id
                        AND eep.node_name = ra.node_name
        INNER JOIN PROJECTION_USAGE pu ON eep.transaction_id = pu.transaction_id AND eep.statement_id = pu.statement_id
WHERE
        qr.start_timestamp > now()::timestamp - INTERVAL '180 minute'       
        AND qp.transaction_id != 0
        AND query NOT LIKE 'select 1'
        AND query NOT LIKE '%search_path%'
        AND eep.counter_name ILIKE 'execution time%'
        AND query LIKE '%/*+ label(monitoring_tpch_query_%'
GROUP BY
        eep.transaction_id, 
        eep.statement_id, 
        qp.query, 
        pu.anchor_table_schema,
        start_timestamp,
        qp.query_duration_us,
        resource_request_execution_ms,        
        qp.reserved_extra_memory,
        ra.memory_inuse_kb             
ORDER BY
        qr.start_timestamp DESC,  
        eep.transaction_id, 
        eep.statement_id
