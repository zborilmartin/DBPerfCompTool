create table if not exists dc_snapshots.query_plan_profiles_snap
as select * from query_plan_profiles
where 1=0
order by transaction_id, statement_id, path_id
segmented by hash(transaction_id) all nodes ksafe;     
