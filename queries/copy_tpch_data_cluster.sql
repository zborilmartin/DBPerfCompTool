COPY myschema.customer FROM 'mypath/customer.tbl'  ON ANY NODE WITH DELIMITER '|' DIRECT;
COPY myschema.nation FROM 'mypath/nation.tbl'  ON ANY NODE WITH DELIMITER '|' DIRECT;
COPY myschema.part FROM 'mypath/part.tbl'  ON ANY NODE WITH DELIMITER '|' DIRECT;
COPY myschema.region FROM 'mypath/region.tbl'  ON ANY NODE WITH DELIMITER '|' DIRECT;
COPY myschema.supplier FROM 'mypath/supplier.tbl'  ON ANY NODE WITH DELIMITER '|' DIRECT;
COPY myschema.orders FROM 'mypath/orders.tbl.1'  ON ANY NODE WITH DELIMITER '|' DIRECT;
COPY myschema.orders FROM 'mypath/orders.tbl.2'  ON ANY NODE WITH DELIMITER '|' DIRECT;
COPY myschema.partsupp FROM 'mypath/partsupp.tbl.1'  ON ANY NODE WITH DELIMITER '|' DIRECT;
COPY myschema.partsupp FROM 'mypath/partsupp.tbl.2'  ON ANY NODE WITH DELIMITER '|' DIRECT;
COPY myschema.lineitem FROM 'mypath/lineitem.tbl.1'  ON ANY NODE WITH DELIMITER '|' DIRECT;
COPY myschema.lineitem FROM 'mypath/lineitem.tbl.2'  ON ANY NODE WITH DELIMITER '|' DIRECT;
COPY myschema.lineitem FROM 'mypath/lineitem.tbl.3'  ON ANY NODE WITH DELIMITER '|' DIRECT;
COPY myschema.lineitem FROM 'mypath/lineitem.tbl.4'  ON ANY NODE WITH DELIMITER '|' DIRECT;
COPY myschema.lineitem FROM 'mypath/lineitem.tbl.5'  ON ANY NODE WITH DELIMITER '|' DIRECT;
COPY myschema.lineitem FROM 'mypath/lineitem.tbl.6'  ON ANY NODE WITH DELIMITER '|' DIRECT;
COPY myschema.lineitem FROM 'mypath/lineitem.tbl.7'  ON ANY NODE WITH DELIMITER '|' DIRECT;

