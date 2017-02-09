insert /*+ direct */ into dc_snapshots.query_plan_profiles_snap
select * from query_plan_profiles where (transaction_id, statement_id, path_id) not in (
  select transaction_id, statement_id, path_id from dc_snapshots.query_plan_profiles_snap
);
commit;   
