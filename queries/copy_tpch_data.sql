COPY myschema.customer FROM 'mypath/customer.tbl'  WITH DELIMITER '|' DIRECT;
COPY myschema.nation FROM 'mypath/nation.tbl'  WITH DELIMITER '|' DIRECT;
COPY myschema.part FROM 'mypath/part.tbl'  WITH DELIMITER '|' DIRECT;
COPY myschema.region FROM 'mypath/region.tbl'  WITH DELIMITER '|' DIRECT;
COPY myschema.supplier FROM 'mypath/supplier.tbl'  WITH DELIMITER '|' DIRECT;
COPY myschema.orders FROM 'mypath/orders.tbl.1'  WITH DELIMITER '|' DIRECT;
COPY myschema.orders FROM 'mypath/orders.tbl.2'  WITH DELIMITER '|' DIRECT;
COPY myschema.partsupp FROM 'mypath/partsupp.tbl.1'  WITH DELIMITER '|' DIRECT;
COPY myschema.partsupp FROM 'mypath/partsupp.tbl.2'  WITH DELIMITER '|' DIRECT;
COPY myschema.lineitem FROM 'mypath/lineitem.tbl.1'  WITH DELIMITER '|' DIRECT;
COPY myschema.lineitem FROM 'mypath/lineitem.tbl.2'  WITH DELIMITER '|' DIRECT;
COPY myschema.lineitem FROM 'mypath/lineitem.tbl.3'  WITH DELIMITER '|' DIRECT;
COPY myschema.lineitem FROM 'mypath/lineitem.tbl.4'  WITH DELIMITER '|' DIRECT;
COPY myschema.lineitem FROM 'mypath/lineitem.tbl.5'  WITH DELIMITER '|' DIRECT;
COPY myschema.lineitem FROM 'mypath/lineitem.tbl.6'  WITH DELIMITER '|' DIRECT;
COPY myschema.lineitem FROM 'mypath/lineitem.tbl.7'  WITH DELIMITER '|' DIRECT;

