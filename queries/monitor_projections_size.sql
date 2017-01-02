select sum(used_bytes) 
from projection_storage 
where projection_schema like 'SCHEMANAME' 
    and anchor_table_name IN ('CUSTOMER', 'LINEITEM', 'NATION', 'ORDERS','PART', 'PARTSUPP','REGION','SUPPLIER') 
group by anchor_table_name 
order by anchor_table_name
