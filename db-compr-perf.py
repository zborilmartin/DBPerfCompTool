#!/usr/bin/env python
import pyodbc
import re
import yaml
import argparse
from sys import exit

class DBPerfComp(object):
    # Method for parsing aguments
    # Arguments:
    #   - Config file
    @staticmethod
    def arg_parser():
        parser = argparse.ArgumentParser(description="DB Performance Comparision tool")
        parser.add_argument('-cf', '--conf_file', default='dbd.yaml', help='Config file to DBPerfTool')
        args = parser.parse_args()
        return args
    
	def __init__(self):
        # Connection to Vertica DB
		self.conn = pyodbc.connect("DSN=vertica")
		self.conn.autocommit = True
        # Setting Config file to attribute confFile
        self.confFile = self.arg_parser().conf_file
        
		#conn = pyodbc.connect('DRIVER={Vertica};SERVER=mzb-vertica72-18.na.intgdc.com;PORT=55076;DATABASE=vertica;UID=vertica;PWD=')
	
    # Extracting query from specific file
	def extract(self,queryName):
        # Queries must be stored in folder 'queries'
		sqlFile = open('queries/%s.sql' % queryName);
        
        # All lines are stored in list
		bffr = []		
		for line in sqlFile:
			bffr.append(line)	
            
        # Joining items of list (lines of query) to one string/statement
		statement = ' '.join(bffr)
		return statement

    
    # Printing info about one row of output table
	def printInfo(self,row,tablename,testname):
		print "-------------------------------"
        print "TABLE NAME: " + tablename
        print "Test: " + testname
        print "Label: " + row[8]
        print "Schema: " + row[0]
        print "Timestamp: " + str(row[1])
        print "Transacton: " + str(row[2])
        print "Statement: " + str(row[3])
        print "Query duration (us): " + str(row[4])
        print "Resource request execution (ms): " + str(row[5])
        print "Used memory (kb): " + str(row[6])
        print "CPU_TIME: " + str(row[7])		

            
    # Method for sending data into the database
	def monitor(self, length, tablename, testname):
        # Storing query for monitoring database 
		monitor_statement = self.extract('monitor')
        # Adding LIMIT -> store data only for that queries that run in one iteration
        monitor_statement += " LIMIT %d" % length
		cursor = self.conn.cursor()
		cursor.execute(monitor_statement)
		rows = cursor.fetchall()
		for row in rows:
			print "........."
			start = row[8].find('/*+ ') + 4
			end = row[8].find(' */')
			label = row[8][start:end]			
			row[8] = label
            
			#cursor.execute("insert into monitoring_output.test2(s,a) values (1,2)")
			# query = "insert into %s  (table_schame,start_timestamp,transaction_id,statement_id,query_duration_us,resource_request_execution_ms,used_memory_kb,CPU_TIME,label) values ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}','{6}', '{7}', '{8}')" % tablename
			#query = query.format(*row)
			#self.printInfo(row,tablename,testname)
			#cursor.execute(query)
			#cursor.commit() 
		cursor.close()
    
    # Method for running specific Query 
    def runQuery(self,listQueries,listSchemas,iteration,testname):
        cursor = self.conn.cursor()
        # Name of schema where to load monitoring data
		monitor_schema = "monitoring_output"
        # Creating schema in database
		cursor.execute("CREATE SCHEMA IF NOT EXISTS %s" % monitor_schema)
        # For each schema which is given in Config file
		for schema in listSchemas:
            # Setting search path to this schema
            # Others schemas are out of quering -> in query, there is no FROM <schema_name>.TABLE -> we eliminate it setting searching path
			schema_statement = "set search_path to \"$user\", public, v_catalog, v_monitor, v_internal, %s" % schema
			# print schema_statement
            
            # Executing SEARCH PATH query
            cursor.execute(schema_statement)
            
            # Loading query for creating table in schema above
			create_table_statement = self.extract('monitor_create')

            # Setting table name which will be in creating query
			tablename = monitor_schema + "." + testname
            
            # In creat-table query is: TABLENAME
            # This text is replaced whith name that we want
			create_table_statement = create_table_statement.replace("TABLENAME", tablename)
            
			# print create_table_statement
            
            # Executing Create-table query
			cursor.execute(create_table_statement)		
            
            # For each iteration which is given in Config file
			for i in range(0,iteration):
                # For each query which is given in Config file
				for query in listQueries:			
                    # Loading query from folder
                    statement = self.extract(query)
                    # Executing given query
					cursor.execute(statement)
                    # Loading data from database
                    rows = cursor.fetchall()
                # Monitoring data    
				self.monitor(len(listQueries), tablename, schema)
                cursor.close()
    
    
    # Parsing YAML configuration file
    def parserYAML(self, file):
        try:
            # Opening file
            yamlFile = open(file)        
            # Loading data from file
            confData = yaml.safe_load(yamlFile)            
            yamlFile.close()
            if not confData:
                raise Exception('Data not loaded')
            # Setting variables querise, testname, iteration, schemas
            self.queries = confData['Conf']['queries']
            self.testname = confData['Conf']['testName']
            self.iteration = confData['Conf']['iteration']
            self.schemas = confData['Conf']['schemas']            
        except IOError as e:
            print "File was not loaded" 
            exit()            
            
	def main(self):
		print self.queries
        print self.testname
        print self.iteration
        print self.schemas
        self.parserYAML(self.confFile)
		self.runQuery(self.queries,self.schemas,self.iteration,self.testname)		

	def __del__(self):
		self.conn.close()

if __name__ == "__main__":
	DBPerfComp().main()

    
#import logging
#logging.basicConfig(level=logging.INFO)
#logger = logging.getLogger(__name__)
#logger.info('Start reading database')
#records = {'john': 55, 'tom': 66}
#logger.debug('Records: %s', records)
