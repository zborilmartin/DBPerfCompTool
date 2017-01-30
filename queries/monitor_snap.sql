-- Author: Jan Soubusta, https://github.com/jaceksan

select
  pu.anchor_table_schema as schema_name,
  ri.time as start_timestamp, 
  nvl(rc.time, getdate()) as endtime,
  ri.transaction_id, 
  ri.statement_id,
  datediff('millisecond', ri.time, nvl(rc.time, getdate())) as response_ms,
  ra.memory_inuse_kb::integer as memory_allocated_kb,
  ra.memory_inuse_kb::integer - (rc.reserved_extra_memory/1024)::integer as memory_used_kb,
  e.cpu_time::integer,
  ri.label
from dc_requests_issued_snap ri
left outer join dc_requests_completed_snap rc
  on ri.node_name = rc.node_name and ri.session_id = rc.session_id and ri.request_id = rc.request_id
left outer join (
  select transaction_id, statement_id, pool_name,
    avg(memory_kb) as memory_inuse_kb, avg(thread_count) as thread_count,
    avg(resource_wait_ms) as resource_wait_ms
  from (
    select a.transaction_id, a.statement_id, a.pool_name, a.node_name,
      first_value(a.memory_kb) over (partition by a.node_name, a.transaction_id, a.statement_id, a.pool_name order by r.acquire_time desc) as memory_kb,
      first_value(a.threads) over (partition by a.node_name, a.transaction_id, a.statement_id, a.pool_name order by r.acquire_time desc) as thread_count,
      datediff('millisecond',
        min(r.queue_time) over (partition by a.node_name, a.transaction_id, a.statement_id, a.pool_name),
        max(r.acquire_time) over (partition by a.node_name, a.transaction_id, a.statement_id, a.pool_name)
      ) as resource_wait_ms,
      row_number() over (partition by a.node_name, a.transaction_id, a.statement_id, a.pool_name order by r.acquire_time desc) as rownum
    from dc_resource_acquisitions_snap a
    join dc_resource_releases_snap r
      on (a.node_name=r.node_name and
           a.transaction_id=r.transaction_id and
           a.statement_id=r.statement_id and
           a.start_time = r.queue_time)
  ) x
  where x.rownum = 1
  group by transaction_id, statement_id, pool_name
) ra
  using (transaction_id, statement_id)
join (
  select transaction_id, statement_id,
    avg(cpu_time) as cpu_time
  from (
    select
      node_name, transaction_id, statement_id,
      round(sum(decode(counter_name, 'execution time (us)', counter_value, 0))/1000) as cpu_time
    from execution_engine_profiles_snap
    group by node_name, transaction_id, statement_id
  ) x
  group by transaction_id, statement_id
) e
  using (transaction_id, statement_id)
inner join projection_usage_snap pu on ri.transaction_id = pu.transaction_id and ri.statement_id = pu.statement_id
where 1=1
  and rc.time is not null -- already finished
  and ri.label = '_QUERY_TESTNAME_SCHEMA_RUNNAME_'
order by start_timestamp desc
