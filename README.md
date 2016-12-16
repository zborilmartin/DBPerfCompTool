# DBPerfCompTool

This DBPerCompTool tool can be used for work with Vertica database and it was written in Python. The main use case of this tool is for testing performance on different schemas. There are also other use cases that the tool can be used for.

## Use cases

## Queries

## Outputs

### Profile path

### Explain 

### Excel file

## Requirements

Requirements are:
**Python** - tested on Python 2.6
Module **Openpyxl** - tested on openpyxl-2.4.1
Module **Pyodbc** - tested on pyodbc-2.1.9

Modules Openpyxl and Pyodbc are included in the file *Requirement*.

## Arguments

The tool can be run with two argument: 
* `-cf` or `--conf_file` - load YAML configuration file.
* `-m` or `--mode` - mode of tool usage

### Configuration file

The configuration file must have structure:

    Conf:
        testName: test
        queries: query1 query2 query3
        schemas: schema1 schema 2
        iteration: 10
        
Configuration may contain several queries and schemas which are separated with space. 

