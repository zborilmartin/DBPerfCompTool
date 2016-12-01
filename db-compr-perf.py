#!/usr/bin/env python
import pyodbc
import re




class DBPerfComp(object):
	def __init__(self):
		self.conn = pyodbc.connect("DSN=vertica")
		self.conn.autocommit = True
		#conn = pyodbc.connect('DRIVER={Vertica};SERVER=localhost;PORT=5433;DATABASE=vertica;UID=vertica;PWD=')
	
	def extract(self,queryNumber):
		sqlFile = open('queries/%s.sql' % queryNumber);
		bffr = []		
		for line in sqlFile:
			bffr.append(line)	
		statement = ' '.join(bffr)
		return statement

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

	def monitor(self, length, tablename, testname):
		monitor_statement = self.extract('monitor')
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
			query = "insert into %s  (table_schame,start_timestamp,transaction_id,statement_id,query_duration_us,resource_request_execution_ms,used_memory_kb,CPU_TIME,label) values ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}','{6}', '{7}', '{8}')" % tablename
			query = query.format(*row)
			self.printInfo(row,tablename,testname)
			cursor.execute(query)
			cursor.commit() 
		cursor.close()

		

        def runQuery(self,listQueries,listSchemas,iteration,testname):
                cursor = self.conn.cursor()
		monitor_schema = "monitoring_output"
		cursor.execute("CREATE SCHEMA IF NOT EXISTS %s" % monitor_schema)
		for schema in listSchemas:
			schema_statement = "set search_path to \"$user\", public, v_catalog, v_monitor, v_internal, %s" % schema
			print schema_statement
			cursor.execute(schema_statement)
			create_table_statement = self.extract('monitor_create')
			name = schema
			tablename = monitor_schema
			tablename += "."
			tablename += testname
			create_table_statement = create_table_statement.replace("TABLENAME", tablename)
			print create_table_statement
			cursor.execute(create_table_statement)		
			for i in range(0,iteration):
				for query in listQueries:			
                			statement = self.extract(query)
					cursor.execute(statement)
                			rows = cursor.fetchall()
				self.monitor(len(listQueries), tablename, schema)
                cursor.close()

	def main(self):
		queries = [1,4]
		schemas = ['tpch_10g']
		iteration = 1
		testname = "test"
		self.runQuery(queries,schemas,iteration,testname)
		

	def __del__(self):
		self.conn.close()





if __name__ == "__main__":
	DBPerfComp().main()
