# DBPerfCompTool
===============
Author is : Martin Zbořil

This DBPerCompTool tool can be used for work with Vertica database and was written in Python. Main use case of this tool is for testing performance on different schemas. There are also other use cases (modes) that the tool can be used for.

## Modes

* Schema comparision
* Schema creation
* Design deployment
* Database Designer - Design creation 
* Design testing

## Requirements

* **Python** - tested on Python 2.6
* Module **Pyodbc** - tested on pyodbc-2.1.9
* Module **Openpyxl** - tested on openpyxl-2.4.1 (if you want to create Excel file in comparison mode)

Modules Openpyxl and Pyodbc are included in the folder *Requirement*.

# Schema comparision

This mode serves for running tests on given schemas. Before running this mode, you must have deployed all schemas that you want to work with.

You must define following attributes in configuration file:
* **testName** - name of the test
* **runName** - name of specific run -  must be unique for every run of the tool
* **queries** - queries to be tested (separated with SPACES)
* **schemas** - schemas to be tested (separated with SPACES)
* **iteration** - number of iterations of each query on each schema
* **excel** - 1 = excel file will be created/data will be added to excel file, 0 = no work with excel file (possible values: 1,0)

Test (testName) is meant for testing different schemas against one specific schema created by Database Designer that is optimized for given queries. E.g. you create schemas with optimized design (by Database Designer) for queries no. 2 and no. 6. Then you create your own schemas definition (try to better optimize it for queries 2 and 6) and deploy it. So there will be queries 2 and 6 in queries attribute in config file. 

The tool runs the queries against the schemas. Then the tool query system tables to have data that you may compere the schemas with. The query is located in the [*`queries`*](./queries)  file and is named [*`monitor_snap`*](./queries/monitor_snap.sql). Important data that are collected and used for comparison are: 
* **response_ms** - time of query run
* **memory_allocated_kb**
* **memory_used_kb**
* **cpu_time**

The tool has also an option to test all TPC-H queries on given schemas (not only few specific queries). The mode is named `COMPARE-ALL`.

## Outputs

### Database

It is better to have multiple iterations to have more precise results. Due to limited memory and retention policy in Vertica, the tool creates and works with snapshots of the system tables. Precise process of the tool is:

1. Run given queries
  * After each iteration of each query insert new data from system tables into snapshot tables
2. After each query the snapshot tables are queried with [*`monitor_snap`*](./queries/monitor_snap.sql) query for required data (memory, time, cpu time)

The data are stored in table (and) that is created by the tool. The schema is `monitoring_output` and the table is `results`. Records in this schema are identified with label. The label contains testName, runName, queries and schemas. Here it is obvious how runName is important. If the runName is the same for several runs of the tool, the data (records) are taken also from different runs and are duplicated in the `results` table.

All columns (data) that are queried from system (snapshot) tables are seen in [*`monitor_create`*](./queries/monitor_create.sql) query that creates a table for storing that data.

### Explain 

The tool stores the Explain and Explain Verbose plans for each schema and given query. The plans are stored in the folder [`ExplainFiles`](./ExplainFiles)`/[testname]`.

### Excel file

The tool may create an excel file where the results are well-arranged and formatted. There are two sheets for each schema - first sheet for normal comparison, second sheet for comparison with ALL TPC-H queries. There, the average values are compared to schema that was created by Database Designer. Explain Verbose plan is included at each schema and query. 

The excel file contain Overview sheet where all needed comparisons are stored. Here you may see which schemas were better (or worse) than the schema created by Database Designer. 

Examples are stored in the folder [`CompareOutput`](./CompareOutput).

# Schema creation

This mode servers for creating schemas with given SQL scripts for schema definition and for copying data to that schema.

E.g. one line in SQL script for copying data:

`COPY myschema.customer FROM 'mypath/customer.tbl'  WITH DELIMITER '|' DIRECT;` 

* *myschema* - is replaced with **name**
* *mypath* - is replaced with **schema_path**

You must define following attributes in configuration file:
* **name** - name of schema to be created
* **data_path** - path where the data are stored
* **schema_path** - path where the schema definition is stored
* **copy_query_path** - path where the script with COPY statements are stored

Paths:
* starts with `'/'` - direct path
* starts without `'/'` - scripts located in the [*`queries`*](./queries) file 

# Design deployment

This mode server for deploying our schema definition to given schema. We must have SQL file that is able to deploy projections (create and refresh new projections, drop old projections) - e.g. output of Database Designer. 

You must define following attributes in configuration file:
* **query_deployment_path** - path where the deployment script is stored
* **previous_schema_occurs** - 1 = occurs, 0 = does not occur - in the scrip may be: `... FROM previous_schema.customer ...` (possible values: 1,0)
* **actual_schema_name** - name of schema where the script is to be deployed
* **previous_schema_name** - name of previous schema (if occurs) - this name will be replaced with **actual_schema_name**

Path:
* starts with `'/'` - direct path
* starts without `'/'` - scripts located in the [*`queries`*](./queries) file 

# Database Designer - Design creation 

This mode servers for creating design with Database Designer build-in tool in Vertica. The functions of Database Designer are called from DBPerfCompTool that takes all necessary attributes from Config file. Complete overview of Database Designer functions is here: [Link to Vertica documentation](https://my.vertica.com/docs/7.1.x/HTML/Content/Authoring/SQLReferenceManual/Functions/VerticaFunctions/DatabaseDesigner/DatabaseDesignerFunctions.htm)

You must define following attributes in configuration file:
* **design_name** - name of design
* **design_schema** - name of schema where the tables are stored
* **tables** - tables that the Database Designer is to be worked on
* **query_path** - path where the queries are stored
* **queries** - queries that the projections are to be optimized for 
* **type** - COMPREHENSIVE (new whole schema) or INCREMENTAL (adding new projections)
* **objective** - focused on: QUERY (high performance), LOAD (small footprint) or BALANCED
* **deploy_path** - path where the deployment script is to be stored
* **deployment** - 1 = design is deployed, 0 = design is only created and not deployed (possible values: 1,0)
* **ksafe** - k-safety of the deployment (insert number)

Detail description of these functions/attributes is in the link above.

You may insert in Type and Objective text that in written in UPPERCASE

Paths:
* starts with `'/'` - direct path
* starts without `'/'` - scripts located in the [*`queries`*](./queries) file 


# Design testing 

This mode serves for automated testing of Database designer. In contrast to Comparison mode, the Design testing mode also creates schemas and design with Database designer and adds queries sets based on achieved results. 

You must define following attributes in configuration file:
* **testName** - name of the test
* **n-tuple** - maximal tuple size of queries sets
* **base_schema** - base schema that is to be compared to
* **base_schema_path** - path where the base schema definition is stored
* **schemas** - schemas that are to be comparing with base_schema (separated with SPACES) 
* **schemas_path** - path where the schemas definition is stored (separated with SPACES)
* **queries** - queries to be tested (separated with SPACES)
* **threshold** - threshold of ratio for adding new queries sets - described below

Design testing mode stores data into the schema `monitoring_design` and table `output`. 

Process:

1. Create query_bucket from queries from the Config file
2. For each query from query_bucket
  1. For each schema that is given in the Config file (including base schema)
    1. Create schema with specific schema definition (not at base schema) 
    2. Create and deploy design for specific query set and specific schema with Database Designer (not at base schema) 
    3. Parse segmentation from designed projections script (at base schema from definition)
    4. Run TPC-H queries from query set on specific schema with iteration 3
    5. Monitor these queries and query system tables for monitoring data (same monitoring as in Comparison mode - response_ms, memory_allocated_kb, memory_used_kb, cpu_time_ms)
    6. For response time (ms) - compute ratio (not at base schema) : response time at this schema / response time at base schema
    7. If ration is lower than **Threshold**, add new query sets to query bucket:
      1. For each query from Config file (**queries**), add query to previous query set, except of the same query - e.g. query set where ratio was lower than threshold has queries [2,3] and in Config files are queries (1,2,3,4,5,6) -> new query sets are [2,3,1], [2,3,4], [2,3,5], [2,3,6]
      2. It runs in this way until the query sets has the maximum length size from Config file (**n-tuple**) - e.g. n-tuple is 4, so there cannot be query sets with 5 queries
    8. Store data to the table `monitoring_design.output` - information from Config file + ratio + monitoring data + segmentation 
      1. [./queries/monitor_design_create.sql](Link to the table definition)
    9. Drop schema
      
Maximal query run is XX minutes, then the query is killed and response time is set to XXX and others monitoring values are XX. 

# Configuration file

## Argument of tool

The tool can be run with an argument: 
* `-cf` or `--conf_file` - load YAML configuration file from [`ConfigFiles`](./ConfigFiles) folder.

Default argument is set to [`ConfigFiles/dbd.yaml`](./ConfigFiles/dbd.yaml).

## Configuration

All attributes in the Config file must be filled. The mode of the tool is configure in attribute `Mode`. You may put several modes separated with space - the modes will be run in sequence. 

### Modes: 

* `COMPARE` - Schema comparision
* `COMPARE-ALL` - Schema comparison - ALL TPC-H queries
* `SCHEMA` - Schema creation
* `DEPLOYMENT` - Design deployment
* `DESIGN` - Database Designer - Design creation 
* `TESTDESIGN` - Design testing


### Example

Example of configuration structure:

    Conf: 
            mode:  SCHEMA DEPLOYMENT COMPARE
    Compare:
            testName: test1
            runName: 1
            queries: 5
            schemas: DBD_test
            iteration: 10
            excel: 0
    Schema: 
            name: myDesign
            data_path: /vertica/tpch/10g
            schema_path: tpch-data-model-basic
            copy_query_path: copy_tpch_data_cluster
    Deployment:
            query_deployment_path: /home/martin.zboril/vertica_output/test_deployment.sql
            previous_schema_occurs: 1
            actual_schema_name: myDesign
            previous_schema_name: DBD_design
    Design:
            design_name: DBD_design
            design_schema: DBD_design
            tables: LINEITEM REGION CUSTOMER PARTSUPP PART ORDERS NATION SUPPLIER
            query_path: /home/vertica/vertica/queriesVertica
            queries: 1 4
            type: COMPREHENSIVE
            objective: BALANCED
            deploy_path: /home/vertica/vertica/output
            deployment: 1       
            ksafe: 1
    TestDesign:
            testName: t1
            n-tuple: 4
            base_schema: design_customized
            base_schema_path: tpch-data-model-vertica_customized
            schemas: dbd_basic dbd_fk dbd_customized
            schemas_path: tpch-data-model-basic tpch-data-model-fk tpch-data-model-vertica_customized
            queries: 1 2 3 4 5 6 7 8 10 11 12 13 14 16 17 18 19 20 21 22 23 24
            threshold: 0.9


