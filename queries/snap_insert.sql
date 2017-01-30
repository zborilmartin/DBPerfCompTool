insert /*+ direct */ into dc_snapshots.dc_requests_issued_snap
select * from dc_requests_issued where (session_id, request_id) not in (
  select session_id, request_id from dc_snapshots.dc_requests_issued_snap
);
commit;

insert /*+ direct */ into dc_snapshots.dc_requests_completed_snap
select * from dc_requests_completed where (session_id, request_id) not in (
  select session_id, request_id from dc_snapshots.dc_requests_completed_snap
);
commit;

insert /*+ direct */ into dc_snapshots.dc_resource_acquisitions_snap
select * from dc_resource_acquisitions where (transaction_id, statement_id) not in (
  select transaction_id, statement_id from dc_snapshots.dc_resource_acquisitions_snap
);
commit;

insert /*+ direct */ into dc_snapshots.dc_resource_releases_snap
select * from dc_resource_releases where (transaction_id, statement_id, request_id) not in (
  select transaction_id, statement_id, request_id from dc_snapshots.dc_resource_releases_snap
);
commit;

insert /*+ direct */ into dc_snapshots.execution_engine_profiles_snap
select * from execution_engine_profiles where (transaction_id, statement_id) not in (
  select transaction_id, statement_id from dc_snapshots.execution_engine_profiles_snap
);
commit;

insert /*+ direct */ into dc_snapshots.projection_usage_snap
select * from projection_usage where (transaction_id, statement_id, request_id, projection_id) not in (
  select transaction_id, statement_id, request_id ,projection_id from dc_snapshots.projection_usage_snap
);
commit;
