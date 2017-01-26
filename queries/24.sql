
select  /*+ label(_24_) */
	n_name,
	l_shipmode,
	c_mktsegment
from
	customer,
	orders,
	lineitem,
	nation,
	supplier	
where
	c_custkey = o_custkey
	and l_orderkey = o_orderkey	
	and n_nationkey = c_nationkey
	and s_suppkey = l_suppkey	
	and o_orderdate >= date '1994-11-01'	
	and c_acctbal > 9000
	and l_quantity > 2
	and n_name LIKE 'A%'
	and s_acctbal > 7000		
	and l_shipmode in ('MAIL', 'REG AIR', 'AIR')
GROUP BY
        n_name,
        l_shipmode,
        c_mktsegment,
        o_orderpriority;
