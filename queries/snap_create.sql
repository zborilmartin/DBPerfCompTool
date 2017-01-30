create table if not exists dc_snapshots.dc_requests_issued_snap
as select * from dc_requests_issued
where 1=0
order by transaction_id, statement_id, request_id
segmented by hash(transaction_id) all nodes ksafe;

create table if not exists dc_snapshots.dc_requests_completed_snap
as select * from dc_requests_completed
where 1=0
-- Vertica support case 00052482
order by session_id, request_id
unsegmented all nodes ksafe;

create table if not exists dc_snapshots.dc_resource_acquisitions_snap
as select * from dc_resource_acquisitions ep
where 1=0
-- Vertica support case 00052482
order by transaction_id, statement_id, node_name, start_time
segmented by hash(transaction_id) all nodes ksafe;

create table if not exists dc_snapshots.dc_resource_releases_snap
as select * from dc_resource_releases ep
where 1=0
order by transaction_id, statement_id, node_name, queue_time
segmented by hash(transaction_id) all nodes ksafe;

create table if not exists dc_snapshots.execution_engine_profiles_snap
as select * from execution_engine_profiles
where 1=0
order by transaction_id, statement_id
segmented by hash(transaction_id) all nodes ksafe;

create table if not exists dc_snapshots.projection_usage_snap
as select * from projection_usage
where 1=0
order by transaction_id, statement_id,request_id, projection_id
segmented by hash(transaction_id) all nodes ksafe;
