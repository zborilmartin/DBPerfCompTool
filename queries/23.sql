
select  /*+ label(__23__LABEL_) */	
	c_name,
	n_name,
	o_orderpriority,
	o_orderstatus,
	count(o_orderkey) as count_orders,
	cast(sum(o_totalprice) as DECIMAL(8,0)) as total_price,
	min(o_orderdate) as min_date,
	max(o_orderdate) as max_date,
	cast(sum(l_quantity) as DECIMAL(4,0)) as quantity
from	
	customer,
	orders,
	lineitem,
	nation
where	
	o_custkey = c_custkey and
	l_orderkey = o_orderkey and 
	o_orderpriority in ('1-URGENT', '2-HIGH') and
	n_regionkey = 3 and 
	n_nationkey = c_nationkey
group by	
	c_name,
	o_orderpriority,
	o_orderstatus,
	n_name
	
order by	
	count_orders DESC, total_price DESC
LIMIT 100;	
