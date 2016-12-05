#!/usr/bin/env python
#import pyodbc
import re
import os
import yaml
import argparse
import logging
from sys import exit
from manageExcel import * 

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
#        	# Connection to Vertica DB
#		self.conn = pyodbc.connect("DSN=vertica")
#		self.conn.autocommit = True
#		# Setting Config file to attribute confFile
		self.confFile = self.arg_parser().conf_file
#		#conn = pyodbc.connect('DRIVER={Vertica};SERVER=mzb-vertica72-18.na.intgdc.com;PORT=55076;DATABASE=vertica;UID=vertica;PWD=')
		
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
			start = row[8].find('/*+ label(') + 10
			end = row[8].find(') */')
			label = row[8][start:end]		
			row[8] = label
            		
			query = "insert into %s  (table_schame,start_timestamp,transaction_id,statement_id,query_duration_us,resource_request_execution_ms,used_memory_kb,CPU_TIME,label) values ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}','{6}', '{7}', '{8}')" % tablename
			query = query.format(*row)
			
			self.printInfo(row,tablename,testname)
			
			cursor.execute(query)
			cursor.commit() 
		cursor.close()
    
	def executeTest(self,iteration,listQueries,cursor,tablename,schema,testname):
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
                                        loadDataToExcel(rows,query,schema,testname)                                            
                                        # Monitoring data    
                                self.monitor(len(listQueries), tablename, schema)

	def executeExplainProfile(self,listQueries,cursor,tablename,schema,testname,output_schema):
		for query in listQueries:
			fileExplain = './ExplainProfile/{0}/Explain_{1}_{2}_{3}.txt'.format(testname,testname,schema,query)
			if not os.path.exists(fileExplain):
				# Loading query from folder
				statement = self.extract(query)

				statement_profile = "PROFILE " + statement
				statement_explain = "EXPLAIN " + statement
				statement_explain_verbose = "EXPLAIN VERBOSE " + statement
			
				if not os.path.exists('./ExplainProfile'):
    					os.makedirs('./ExplainProfile')
				if not os.path.exists('./ExplainProfile/%s' % testname):
                                	os.makedirs('./ExplainProfile/%s' % testname)	

				# Executing PROFILE QUERY
				cursor.execute(statement_explain)
				# Loading data from database
				rows = cursor.fetchall()
				
				with open(fileExplain, "w+") as explainFile:
					for row in rows:
						explainFile.write(row[0]+'\n')
				explainFile.close()

                                fileVerboseExplain = './ExplainProfile/{0}/VerboseExplain_{1}_{2}_{3}.txt'.format(testname,testname,schema,query)

                                if not os.path.exists(fileVerboseExplain):

					# Executing EXPLAIN VERBOSE QUERY
					cursor.execute(statement_explain_verbose)
					# Loading data from database
					rows = cursor.fetchall()

                                	with open(fileVerboseExplain, "w+") as explainVerboseFile:
                                        	for row in rows:
                                                	explainVerboseFile.write(row[0]+'\n')
                                	explainVerboseFile.close()
			
				# Loading query for creating table in schema above
				create_table_statement = self.extract('monitor_profile_create')

				# Setting table name which will be in creating query
				tablename = '{0}.{1}_{2}_{3}'.format(output_schema,testname,schema,query)
					    
				# In creat-table query is: TABLENAME
				# This text is replaced whith name that we want
				create_table_statement = create_table_statement.replace("TABLENAME", tablename)
					    
				# print create_table_statement
					    
				# Executing Create-table query
				cursor.execute(create_table_statement)	



				statement = self.extract(query)
				statement_profile = "PROFILE " + statement
				# Executing PROFILE QUERY
				cursor.execute(statement_profile)		
				rows = cursor.fetchall()	
				cursor.execute("SELECT transaction_id, statement_id FROM QUERY_PROFILES WHERE query ILIKE 'PROFILE%' ORDER BY query_start DESC LIMIT 1")

				# Loading data from database
				rows = cursor.fetchall()

				TRANS_ID = rows[0][0]
				STATEM_ID = rows[0][1]

				# Loading query for profile output
				monitor_statement_statement = self.extract('monitor_profile')
				
				 # In creat-table query is: TRANSACTION_NUMBER,STATEMENT_NUMBER
				 # This text is replaced with name that we want
				monitor_statement_statement = monitor_statement_statement.replace("TRANSACTION_NUMBER", str(TRANS_ID))
				monitor_statement_statement = monitor_statement_statement.replace("STATEMENT_NUMBER", str(STATEM_ID))
				monitor_statement_statement = monitor_statement_statement.replace("running_time", "running_time::VARCHAR")
				monitor_statement_statement = monitor_statement_statement.replace("memory_allocated_bytes", "memory_allocated_bytes::VARCHAR")
				monitor_statement_statement = monitor_statement_statement.replace("read_from_disk_bytes", "read_from_disk_bytes::VARCHAR")


				# Executing MONITOR PROFILE QUERY
				cursor.execute(monitor_statement_statement)

				# Loading data from database
				rows = cursor.fetchall()

				for row in rows:
					query = "INSERT INTO TABLENAME (running_time,memory_allocated_bytes,read_from_disk_bytes,path_line) VALUES ('{0}','{1}','{2}','{3}')"
					row[3] = row[3].replace("'", "/")
					query = query.format(*row)
					query = query.replace("TABLENAME", tablename)
					cursor.execute(query)
					cursor.commit()
                    
                #duplicatePattern()
				
		    #loadProfileToExcel(listQueries,tablename,schema,testname,output_schema)

	# Method for running specific Query 
	def runQuery(self,listQueries,listSchemas,iteration,testname,output_schema):
		cursor = self.conn.cursor()
        	
		# Output_schema =  Name of schema where to load monitoring data
	        # Creating schema in database
		cursor.execute("CREATE SCHEMA IF NOT EXISTS %s" % output_schema)
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
			tablename = output_schema + "." + testname
		    
			# In creat-table query is: TABLENAME
			# This text is replaced whith name that we want
			create_table_statement = create_table_statement.replace("TABLENAME", tablename)
		    
			# Executing Create-table query
			cursor.execute(create_table_statement)		
	
			if output_schema == "monitoring_output":
				self.executeTest(iteration,listQueries,cursor,tablename,schema,testname)
			
			if output_schema == "monitoring_profiles":
				self.executeExplainProfile(listQueries,cursor,tablename,schema,testname,output_schema)
                cursor.close()
                
                
                
                
    	def parserYAML(self, file):
        	try:
			# Opening file
			file = "ConfigFiles/" + file
			yamlFile = open(file)        
			# Loading data from file
			confData = yaml.safe_load(yamlFile)            
			yamlFile.close()
			if not confData:
				raise Exception('Data not loaded')
			# Setting variables querise, testname, iteration, schemas
			queries_unparsed = confData['Conf']['queries']
			if type(queries_unparsed) is int:                            
                    		self.queries = [str(queries_unparsed)]                
            		else:                    
 	                	queries_unparsed2 = "".join(queries_unparsed)
			        self.queries = queries_unparsed2.split()


	
	     	        testname_unparsed = confData['Conf']['testName']
			self.testname = "".join(testname_unparsed)

			self.iteration = confData['Conf']['iteration']

			schemas_unparsed = confData['Conf']['schemas']
			schemas_unparsed2 = "".join(schemas_unparsed)
			self.schemas = schemas_unparsed2.split()
            
		except IOError as e:
		    	print "File was not loaded" 
		    	exit()  
	    
	def main(self):
		logging.basicConfig(level=logging.INFO)
		logger = logging.getLogger("DBD_Comp_Perf_Tool")

		self.parserYAML(self.confFile)
		logger.info('Arguments parsed')		
		print self.testname
		logger.info('Testname: %s' % self.testname)
		logger.info('Iteration: %s' % self.iteration)
		logger.info('Number of schemas: %s' % len(self.schemas))
		for schema in self.schemas:
			logger.info('Schema: %s' % schema)
		logger.info('Number of queries: %s' % len(self.queries))	
		for query in self.queries:
			logger.info('Query: %s' % query)
            	createExcelFile(self.testname, self.queries)
		#self.runQuery(self.queries,self.schemas,self.iteration,self.testname,"monitoring_profiles")		
        	rows = ['1','1','1','1','1','1','1']
        	loadDataToExcel(rows,"1","DBD","test",self.queries)
            	loadDataToExcel(rows,"4","DBD","test",self.queries)
            	loadDataToExcel(rows,"1","DBD","test",self.queries)
                
                duplicatePattern("DBD",self.testname,self.queries)
                duplicatePattern("new",self.testname,self.queries)
                loadDataToExcel(rows,"1","new","test",self.queries)
            	#self.runQuery(self.queries,self.schemas,self.iteration,self.testname,"monitoring_output")

        	
	
#	def __del__(self):
#		self.conn.close()

if __name__ == "__main__":
	DBPerfComp().main()

    
#import logging
#logging.basicConfig(level=logging.INFO)
#logger = logging.getLogger(__name__)
#logger.info('Start reading database')
#records = {'john': 55, 'tom': 66}
#logger.debug('Records: %s', records)
