#!/usr/bin/env pytho
import pyodbc
import re
import os
import yaml
import time
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
        	parser = argparse.ArgumentParser(description="DB Performance Comparison tool")
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
		# If query does not end with '.sql', it is added
		if (len(str(queryName)) < 4) or (str(queryName)[-4:] != '.sql'):
			queryName = str(queryName) + '.sql'

		# If query does not start with '/', it takes queries from the file 'queries' 
		if str(queryName)[0] == '/':
			sqlFile = open('%s' % queryName);
		else:
			sqlFile = open('queries/%s' % queryName);
		
		self.logger.info('[EXTRACT QUERY] Query path or file in "queries" file: ' + queryName)

		# All lines are stored in list
		bffr = []		
		for line in sqlFile:
			bffr.append(line)	
		    
		# Joining items of list (lines of query) to one string/statement
		statement = ' '.join(bffr)
		return statement

    
    	# Printing info about one row of output table
	def logInfo(self,row,tablename,testname,query):
		self.logger.info("[MONITORING QUERY] Table name: " + tablename)
		self.logger.info("[MONITORING QUERY] Test: " + testname)
		self.logger.info("[MONITORING QUERY] Label/query: " + row[9])
		self.logger.info("[MONITORING QUERY] Schema (path): " + row[0])
		self.logger.info("[MONITORING QUERY] Start timestamp: " + str(row[1]))
		self.logger.info("[MONITORING QUERY] End timestamp: " + str(row[2]))
		self.logger.info("[MONITORING QUERY] Transaction_id: " + str(row[3]))
		self.logger.info("[MONITORING QUERY] Statement_id: " + str(row[4]))
		self.logger.info("[MONITORING QUERY] Query duration (ms): " + str(row[5]))
		self.logger.info("[MONITORING QUERY] Allocated memory (kb): " + str(row[6]))
		self.logger.info("[MONITORING QUERY] Used memory (kb): " + str(row[7]))
		self.logger.info("[MONITORING QUERY] CPU time: " + str(row[8])+'\n')

            
	# Method for sending data into the database
    	# calling method loadDataToExcel - loading data from monitoring into excel file
	def monitor(self, length, tablename, testname,schema,query,listQueries,runname,tpch=0):
		self.logger.info('Query monitoring started')
        	# Extracting monitoring query
	   	# In the statement, the LABEL must be replaced 
		monitor_statement = self.extract('monitor_snap')
		label = ""

		# Label in form __query__testname__schema__runname__ for test with single queries
		if tpch == 0:	
			label = "__{0}__{1}__{2}__{3}__".format(query,testname,schema,runname)

		# Label in form __testname__schema__runname__ for test with all TPC-H queries
		else:
			tmp_schema =  schema[:-4]
			label = "%__{0}__{1}__{2}__".format(testname,tmp_schema,runname)
			monitor_statement = monitor_statement.replace("ri.label = '","ri.label ILIKE '")

		self.logger.info('Label monitoring: ' + label)
		monitor_statement = monitor_statement.replace("_LABEL_",label)

		#self.logger.info('Monitoring query: \n' + monitor_statement)

		cursor = self.conn.cursor()
		cursor.execute(monitor_statement)
		rows = cursor.fetchall()
        
                # Creating new sheet in specific XLSX file 
                duplicatePattern(schema,testname,listQueries,query)

		# Sending Explain Verbose output to Excel
                loadExplain(schema,testname,rows,listQueries,query,1)            

		# Sending monitor data to Excel
           	loadDataToExcel(rows,query,schema,testname,listQueries,tpch)
		
		self.logger.info('Size of rows: ' + str(len(rows)))

        	# Sending data to the database
		for row in rows:	
			query_statement = "insert into %s  (schema_name,start_timestamp,end_timestamp,transaction_id,statement_id,response_ms,memory_allocated_kb,memory_used_kb,cpu_time_ms,label) values ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}','{6}', '{7}', '{8}','{9}')" % (tablename)
			query_statement = query_statement.format(*row)
			#self.logger.info('[MONITORING QUERY] Monitoring query statement: ' + query_statement)
			self.logInfo(row,tablename,schema,query)
			
			cursor.execute(query_statement)
			cursor.commit() 
		cursor.close()

	# Method for executing TPC-H queries and monitoring them 
	def executeTest(self,iteration,listQueries,cursor,tablename,schema,testname,runname,tpch=0):

		# Creation of snapshot tables for storing monitoring data
		self.logger.info('Snapshot tables being created')		
		statement = self.extract('snap_create')
		cursor.execute(statement)


		self.logger.info('Execute test')
                for query in listQueries:
			self.logger.info('[EXECUTE TEST] Query: ' + query)
			# For each iteration which is given in Config file
                	for i in range(0,iteration):
				self.logger.info('[EXECUTE TEST] Iteration n.: ' + str(i+1))

				# In this step, running TPC-H query
				if tpch == 0:
	                                # Loading query from folder
	                                statement = self.extract(query)

					# Replacement of query
					label = "_{0}__{1}__{2}__".format(testname,schema,runname)
					self.logger.info('Label query: __' + query+ label)
					statement = statement.replace("_LABEL_",label)

					# Executing given query
					#self.logger.info('[EXECUTE TEST] Execute query statement: ' + statement)
					cursor.execute(statement)
					rows = cursor.fetchall()
					self.logger.info('[EXECUTE TEST] Number of rows of result: ' + str(len(rows)))

					statement = self.extract('snap_insert')
					self.logger.info('Inserting data to snapshot tables (from system tables)')
					#self.logger.info('Snap insert statements \n' + statement)
					cursor.execute(statement)
				#self.logger.info('[EXECUTE TEST] Iteration finished')
				else:
					schema_tmp = schema + '-ALL'
					for j in range(1,23):
						self.logger.info('[EXECUTE TEST] [ALL - TPC-H queries mode] Query n.: ' + str(j) + ' (iteration n.: ' + str(i+1) + ')')
						statement = self.extract(j)
						label = "_{0}__{1}__{2}__".format(testname,schema,runname)
	                                        self.logger.info('Label query: __' + query+ label)
        	                                statement = statement.replace("_LABEL_",label)
						#self.logger.info('[EXECUTE TEST] Execute query statement: ' + statement)
						cursor.execute(statement)
			                        statement = self.extract('snap_insert')
                        	                cursor.execute(statement)
						self.logger.info('[EXECUTE TEST] Query finished \n')

			# In this step, monitoring executed query
			if tpch == 0:
				self.monitor(len(listQueries), tablename,testname,schema,query,listQueries,runname)		
			else:
				self.monitor(len(listQueries), tablename,testname,schema_tmp,1,listQueries,runname,1)

			self.logger.info('[EXECUTE TEST] Monitoring finished \n')


	# Method for executing EXPLAIN, EXPLAIN VERBOSE and getting projections size
	# Storing data into file 'ExplainFiles/(testname)'
	def executeExplain(self,listQueries,cursor,tablename,schema,testname,output_schema,tpch=0):
		# Files creation
		if not os.path.exists('./ExplainFiles'):
			os.makedirs('./ExplainFiles')
		if not os.path.exists('./ExplainFiles/%s' % testname):
			os.makedirs('./ExplainFiles/%s' % testname)

	
                fileSize = './ExplainFiles/{0}/Projection_size_{1}_{2}.txt'.format(testname,testname,schema)	
		if not os.path.exists(fileSize):	
			self.logger.info('Projection size file is being created')	
			monitor_statement_statement = self.extract('monitor_projections_size')
			monitor_statement_statement = monitor_statement_statement.replace("SCHEMANAME", schema)
					
	 
			# Executing MONITOR PROJECTION SIZE
			cursor.execute(monitor_statement_statement)

			# Loading data from database
			rows = cursor.fetchall()
			
			# Writing Explain into file
			with open(fileSize, "w+") as sizeFile:
				totalSize = 0
				for row in rows:
					size = str(row[0]).split('.')
					sizeFile.write(size[0]+'\n')
					totalSize = totalSize + int(size[0])
				sizeFile.write(str(totalSize)+'\n')
			sizeFile.close()


		for query in listQueries:
			self.logger.info('[Execute Explain Profile] Query: ' + query)

            		# Setting path of the output for Explain
			fileExplain = './ExplainFiles/{0}/Explain_{1}_{2}_{3}.txt'.format(testname,testname,schema,query)
			fileVerboseExplain = './ExplainFiles/{0}/VerboseExplain_{1}_{2}_{3}.txt'.format(testname,testname,schema,query)

            		# The rest of this method is executed only if the statement is true
            		# Important assumption: if there is no Explain file, there is also no Explain Verbose file, Query Profile Plan in the database and EXCEL (XLSX) sheet in the Excel file (and vice versa)
			if (not os.path.exists(fileExplain)) or (not os.path.exists(fileVerboseExplain)):
				# Loading query from folder
				statement = self.extract(query)
                
                		# Adding prefixes to query
				statement_explain = "EXPLAIN " + statement
				statement_explain_verbose = "EXPLAIN VERBOSE " + statement

				# Executing EXPAIN QUERY
				cursor.execute(statement_explain)
				# Loading data from database
				rows = cursor.fetchall()
				
                		# Writing Explain into file
				with open(fileExplain, "w+") as explainFile:
					for row in rows:
						explainFile.write(row[0]+'\n')
				explainFile.close()

				rows_explain = []			

                                if not os.path.exists(fileVerboseExplain):

					# Executing EXPLAIN VERBOSE QUERY
					cursor.execute(statement_explain_verbose)
					# Loading data from database
					rows = cursor.fetchall()

                                        # Writing into Explain Verbose file
                                	with open(fileVerboseExplain, "w+") as explainVerboseFile:
                                        	for row in rows:
                                                	explainVerboseFile.write(row[0]+'\n')
                                	explainVerboseFile.close()

					rows_explain = rows

	           		# Creating new sheet in specific XLSX file 
                		duplicatePattern(schema,testname,listQueries,query)
                        	# Loading profile path to Excel
                		loadExplain(schema,testname,rows_explain,listQueries,query)		    
	


	# Method for running specific Query 
	def runQuery(self,listQueries,listSchemas,iteration,testname,output_schema,runname,tpch=0):
		cursor = self.conn.cursor()
        	self.logger.info('Running query')

		# Output_schema =  Name of schema where to load monitoring data
	        # Creating schema in database
		cursor.execute("CREATE SCHEMA IF NOT EXISTS %s" % output_schema)

       		# For each schema which is given in Config file
		for schema in listSchemas:
			self.logger.info('Actual schema:' + schema)
			# Setting search path to this schema
			# Others schemas are out of quering -> in query, there is no FROM <schema_name>.TABLE -> we eliminate it setting searching path
			cursor.execute('create schema if not exists dc_snapshots')
			schema_statement = "set search_path to %s, dc_snapshots, v_catalog, v_monitor, v_internal" % schema
		    	
			# Executing SEARCH PATH query
			cursor.execute(schema_statement)
				
			self.logger.info('[SET SEARCH PATH] Query: \n' + schema_statement)			
		    
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
				self.executeTest(iteration,listQueries,cursor,tablename,schema,testname,runname,tpch)
			
			if output_schema == "monitoring_explain":
				self.executeExplain(listQueries,cursor,tablename,schema,testname,output_schema,tpch)
                cursor.close()
                

	# Method for parsing arguments from CONFIG file	
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

                        mode_unparsed = confData['Conf']['mode']
                        self.modes = []
                        mode_unparsed2 = "".join(mode_unparsed)
                        self.modes = mode_unparsed2.split()

			for mode in self.modes:
				if mode.upper() not in ('COMPARE','SCHEMA','DESIGN','COMPARE-ALL','DEPLOYMENT'):
					self.logger.error('Error in configuration file. Attribute not passed. Should be only COMPARE,COMPARE-ALL,SCHEMA,DESIGN,DEPLOYMENT')
					quit()
            
			queries_unparsed = confData['Compare']['queries']
			if type(queries_unparsed) is int:                            
                    		self.queries = [str(queries_unparsed)]                
            		else:                    
 	                	queries_unparsed2 = "".join(queries_unparsed)
			        self.queries = queries_unparsed2.split()
	
	     	        testname_unparsed = confData['Compare']['testName']
			self.testname = "".join(testname_unparsed)
            
	     	        runname_unparsed = confData['Compare']['runName']
			self.runname = "".join(str(runname_unparsed))            

			self.iteration = confData['Compare']['iteration']

			schemas_unparsed = confData['Compare']['schemas']
			schemas_unparsed2 = "".join(schemas_unparsed)
			self.schemas = schemas_unparsed2.split()
 
                        name_unparsed = confData['Schema']['name']
                        self.name = "".join(name_unparsed)

                        data_path_unparsed = confData['Schema']['data_path']
                        self.data_path = "".join(data_path_unparsed)

                        schema_path_unparsed = confData['Schema']['schema_path']
                        self.schema_path = "".join(schema_path_unparsed)
            
                        copy_query_path_unparsed = confData['Schema']['copy_query_path']
                        self.copy_query_path = "".join(copy_query_path_unparsed)

                        design_name_unparsed = confData['Design']['design_name']
                        self.design_name = "".join(design_name_unparsed)
                        
                        query_path_unparsed = confData['Design']['query_path']
                        self.query_path = "".join(query_path_unparsed)

                        type_unparsed = confData['Design']['type']
                        self.typeDesign = "".join(type_unparsed)

                        if self.typeDesign.upper() not in ('INCREMENTAL','COMPREHENSIVE'):
                                self.logger.error('Error in configuration file. Attribute not passed. Should be only COMPREHENSIVE, INCREMENTAL')
                                quit()

                        objective_unparsed = confData['Design']['objective']
                        self.objective = "".join(objective_unparsed)

                        if self.objective.upper() not in ('BALANCED','QUERY','LOAD'):
                                self.logger.error('Error in configuration file. Attribute not passed. Should be only BALANCED, QUERY, LOAD')
				quit()

                        deploy_path_unparsed = confData['Design']['deploy_path']
                        self.deploy_path = "".join(deploy_path_unparsed)

                        self.deployment = confData['Design']['deployment']
                        
                        if self.deployment not in (0,1):
                                self.logger.error('Error in configuration file. Attribute not passed. Should be only 1 (true) or  0 (false)')                        
				quit() 

                        design_schema_unparsed= confData['Design']['design_schema']
                        self.design_schema = "".join(design_schema_unparsed)    
                        
                        design_queries_unparsed = confData['Design']['queries']
                        self.design_queries = []
			if type(design_queries_unparsed) is int:
                                self.design_queries = [str(design_queries_unparsed)]
                        else:
                                design_queries_unparsed2 = "".join(design_queries_unparsed)
                                self.design_queries = design_queries_unparsed2.split()

                        tables_unparsed = confData['Design']['tables']
                        tables_unparsed2 = "".join(tables_unparsed)
                        self.tables = tables_unparsed2.split()

                        query_deployment_path_unparsed = confData['Deployment']['query_deployment_path']
                        self.query_deployment_path = "".join(query_deployment_path_unparsed)

                        self.previous_schema_occurs = confData['Deployment']['previous_schema_occurs']

                        actual_schema_name_unparsed= confData['Deployment']['actual_schema_name']
                        self.actual_schema_name = "".join(actual_schema_name_unparsed)

                        previous_schema_name_unparsed= confData['Deployment']['previous_schema_name']
                        self.previous_schema_name = "".join(previous_schema_name_unparsed)		

		except IOError as e:
		    	print "File was not loaded" 
		    	exit() 


	# Method for creating new schema - SCHEMA mode
	def createSchema(self,name,data,schema,copy_query):
                cursor = self.conn.cursor()

		# Loading file where the query for creating schema is stored
		# To be universal, in the query you may insert 'myschema' as schema for all tables -> 'myschema' is replaced with inserted schema name into the config file
		statement = self.extract(schema)
		cursor.execute("CREATE SCHEMA IF NOT EXISTS {0}".format(name))
		statement = statement.replace("myschema", name)

		#self.logger.info('[SCHEMA] CREATE SCHEMA QUERY \n: ' + statement)
		self.logger.info('[SCHEMA] Schema is being created')
		cursor.execute(statement)
		self.logger.info('[SCHEMA] DONE - CREATE SCHEMA')

		# Loading file where the query for copying data is stored
                statement2 = self.extract(copy_query)
                statement2 = statement2.replace("myschema", name)
                statement2 = statement2.replace("mypath", data)
                #self.logger.info('[SCHEMA] COPY DATA QUERY \n: ' + statement2)
		self.logger.info('[SCHEMA] Data are being copied')
		cursor.execute(statement2)
		self.logger.info('[SCHEMA] DONE - COPY DATA')


	# Method for creating new DB design - DESIGN mode
	def createDesign(self,design_name,query_path,typeDesign,objective,deploy_path,deployment,tables,design_queries,schema):
                cursor = self.conn.cursor()
		try:
			cursor.execute("SELECT DESIGNER_DROP_DESIGN('{0}')").format(design_name)   
			time.sleep(5)
			self.logger.info('[DESIGN] Desing ' + design_name + ' was dropped')
		except Exception as e:
			try:
				cursor.execute("select dbd_drop_all_workspaces('DESIGNER')")
			except Exception as e:
				self.logger.info('[DESIGN] Desing did not exist before')
		# Extracting all table names of schema
		cursor.execute("SELECT DESIGNER_CREATE_DESIGN('{0}')".format(design_name))
		self.logger.info('[DESIGN] SELECT DESIGNER_CREATE_DESIGN: ' + design_name )
		for table in tables:
			cursor.execute("SELECT DESIGNER_ADD_DESIGN_TABLES('{0}','{1}.{2}')".format(design_name,schema,table))
			self.logger.info('[DESIGN] DESIGNER_ADD_DESIGN_TABLES: ' + table)
		for query in design_queries:
			cursor.execute("SELECT DESIGNER_ADD_DESIGN_QUERIES('{0}', '{1}/{2}.sql','true')".format(design_name,query_path,query))
			self.logger.info('[DESIGN] DESIGNER_ADD_DESIGN_QUERIES: ' + str(query))
			self.logger.info("SELECT DESIGNER_ADD_DESIGN_QUERIES('{0}', '{1}/{2}.sql','true')".format(design_name,query_path,query))
		cursor.execute("SELECT DESIGNER_SET_DESIGN_TYPE('{0}', '{1}')".format(design_name,typeDesign))
		self.logger.info('[DESIGN] DESIGNER_SET_DESIGN_TYPE: ' + typeDesign)
		cursor.execute("SELECT DESIGNER_SET_OPTIMIZATION_OBJECTIVE('{0}', '{1}')".format(design_name,objective))
		self.logger.info('[DESIGN] DESIGNER_SET_OPTIMIZATION_OBJECTIVE: ' + objective)
		cursor.execute("SELECT DESIGNER_RUN_POPULATE_DESIGN_AND_DEPLOY ('{0}', '{1}/{2}_projections.sql', '{3}/{4}_deploy.sql', true, {5}, true, true)".format(design_name,deploy_path,design_name,deploy_path,design_name,deployment))
		self.logger.info('[DESIGN] DESIGNER_RUN_POPULATE_DESIGN_AND_DEPLOY: path = ' + deploy_path)
		self.logger.info('[DESIGN] Desing created')

	# Method for deployment - DELPOYMENT mode
	def deploy(self,query_deployment_path,previous_schema_occurs,actual_schema_name,previous_schema_name):
		cursor = self.conn.cursor()

		# Extracting deployment query
		statement = self.extract(query_deployment_path)

		# If 1 - replacement of old schema name with new schema name in deployment query 
		if previous_schema_occurs == 1:
	                statement = statement.replace(previous_schema_name, actual_schema_name)
			self.logger.info('[CONFIG-DEPLOYMENT] Previous schema name: ' + previous_schema_name)
            	self.logger.info('[DEPLOYMENT] Deployment in progress')
		cursor.execute(statement)
		self.logger.info('[DEPLOYMENT] Query executed')


	# Method for verifying input from config file
	def verifyInput(self):
		userInput = ""
		while True:
			userInput = raw_input("Please confirm parameters from your Config file (yes/no): ")	
			if userInput.upper() in ["Y","YE","YES"]:
				print "Parameters confirmed"
				return True
			elif userInput.upper() in ["N","NO"]:
				print "Parameters not confirmed. Program exit."
				return False
			else:
				print "Please insert yes or no!"

	def main(self):
		logging.basicConfig(level=logging.INFO)
		self.logger = logging.getLogger("DBD_Comp_Perf_Tool")
		
		# Parsing arguments
		self.parserYAML(self.confFile)
	
		# Tool may be executed in several MODES
		for mode in self.modes:
			self.logger.info('[CONFIG] Mode: %s' % mode)
                        if mode.upper() == 'COMPARE' or mode.upper() == 'COMPARE-ALL':	
				self.logger.info('[CONFIG-COMPARE] Testname: %s' % self.testname)
 		                self.logger.info('[CONFIG-COMPARE] Runname: %s' % self.runname)
				self.logger.info('[CONFIG-COMPARE] Iteration: %s' % self.iteration)
				self.logger.info('[CONFIG-COMPARE] Number of schemas: %s' % len(self.schemas))
				for schema in self.schemas:
					self.logger.info('[CONFIG-COMPARE] Schema: %s' % schema)
				self.logger.info('[CONFIG-COMPARE] Number of queries: %s' % len(self.queries))	
				for query in self.queries:
					self.logger.info('[CONFIG-COMPARE] Query: %s' % query)
			if mode.upper() == 'COMPARE':
				if self.verifyInput() == False:
					exit()
				createExcelFile(self.testname, self.queries)
				self.runQuery(self.queries,self.schemas,self.iteration,self.testname,"monitoring_explain",self.runname)		
				self.runQuery(self.queries,self.schemas,self.iteration,self.testname,"monitoring_output",self.runname)
			if mode.upper() == 'COMPARE-ALL':
                                if self.verifyInput() == False:
                                        exit()
				createExcelFile(self.testname, self.queries)
				self.runQuery(['tpch_small'],self.schemas,self.iteration,self.testname,"monitoring_output",self.runname,1)
			if mode.upper() == 'SCHEMA':
				self.logger.info('[CONFIG-SCHEMA] Schema name: %s' % self.name)
				self.logger.info('[CONFIG-SCHEMA] Path of data to copy to database: %s' % self.data_path)
				self.logger.info('[CONFIG-SCHEMA] Path of schema to create: %s' % self.schema_path)
				self.logger.info('[CONFIG-SCHEMA] Path of copy query: %s' % self.copy_query_path)
                                if self.verifyInput() == False:
                                        exit()
				self.createSchema(self.name,self.data_path,self.schema_path,self.copy_query_path)
			if mode.upper() == 'DESIGN':
				self.logger.info('[CONFIG-DESIGN] Deisng name: ' + self.design_name)
				self.logger.info('[CONFIG-DESIGN] Query path: ' +  self.query_path)
				self.logger.info('[CONFIG-DESIGN] Design type: ' + self.typeDesign)
				self.logger.info('[CONFIG-DESIGN] Objective: ' +  self.objective)
				self.logger.info('[CONFIG-DESIGN] Deploy path: ' + self.deploy_path)
				self.logger.info('[CONFIG-DESIGN] Deployment - 1-true/0-false: ' + str(self.deployment))
				for table in self.tables:
					self.logger.info('[CONFIG-DESIGN] Table: ' + table)
				for query in self.design_queries:
					self.logger.info('[CONFIG-DESIGN] Query: ' + query)
				self.logger.info('[CONFIG-DESIGN] Design schema: ' + self.design_schema)
                                if self.verifyInput() == False:
                                        exit()
				self.createDesign(self.design_name, self.query_path, self.typeDesign, self.objective, self.deploy_path, self.deployment, self.tables,self.design_queries,self.design_schema)
			if mode.upper() == 'DEPLOYMENT':
				self.logger.info('[CONFIG-DEPLOYMENT] Query path: ' + self.query_deployment_path)
				self.logger.info('[CONFIG-DEPLOYMENT] Actual schema name: ' + self.actual_schema_name)
				self.logger.info('[CONFIG-DEPLOYMENT] Previous schema occurs (1-true/0-false): ' + str(self.previous_schema_occurs))
                                #if self.verifyInput() == False:
                                #        exit()
				self.deploy(self.query_deployment_path,self.previous_schema_occurs,self.actual_schema_name,self.previous_schema_name)

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
