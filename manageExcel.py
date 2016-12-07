#!/usr/bin/env python
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font, Color,PatternFill
from openpyxl.styles import colors
from openpyxl.formatting.rule import ColorScaleRule, CellIsRule, FormulaRule
from openpyxl.styles.differential import DifferentialStyle
from openpyxl.formatting import Rule
from openpyxl import load_workbook    
import os

# Setting colors and fonts
blueFill = PatternFill(start_color="1EB4F5",end_color="1EB4F5",fill_type='solid')
orangeFill = PatternFill(start_color="FFB011",end_color="FFB011",fill_type='solid')
yellowFill = PatternFill(start_color="FFF811",end_color="FFF811",fill_type='solid')
redFill = PatternFill(start_color="FF0000",end_color="FF0000",fill_type='solid')
greenFill = PatternFill(start_color="07EE1E",end_color="07EE1E",fill_type='solid')
darkredFill = PatternFill(start_color="990000",end_color="990000",fill_type='solid')
pinkFill = PatternFill(start_color="FF66B2",end_color="FF66B2",fill_type='solid')
lightblueFill = PatternFill(start_color="99FFFF",end_color="99FFFF",fill_type='solid')
brownFill = PatternFill(start_color="994C00",end_color="994C00",fill_type='solid')
lightgreenFill = PatternFill(start_color="CCFFCC",end_color="CCFFCC",fill_type='solid')
greyFill = PatternFill(start_color="C0C0C0",end_color="C0C0C0",fill_type='solid')
bold = Font(bold=True)
bold22 = Font(bold=True,size=22)
bold36 = Font(bold=True,size=36)

# Method for setting red or green fill -> is greater or smaller than particular cell
def formatRedGreenFill(ws,dbd,row_comparing,column_comparing,row_to_compare,column_to_compare):
	ws.conditional_formatting.add('{0}'.format(ws.cell(row=row_comparing, column=column_comparing).coordinate), CellIsRule(operator='greaterThan', formula=['DBD!${0}'.format(dbd.cell(row=row_to_compare, column=column_to_compare).coordinate)], stopIfTrue=True, fill=redFill))
        ws.conditional_formatting.add('{0}'.format(ws.cell(row=row_comparing, column=column_comparing).coordinate), CellIsRule(operator='lessThan', formula=['DBD!${0}'.format(dbd.cell(row=row_to_compare, column=column_to_compare).coordinate)], stopIfTrue=True, fill=greenFill))  

# Method for setting deferences on two metrics        
# Difference is situated one cell under comparing metrics
def formatDifference(ws,dbd,row_comparing,column_comparing,row_to_compare,column_to_compare):
        ws['{0}'.format(ws.cell(row=row_comparing+1, column=column_comparing).coordinate)] = "=DBD!{0}-{1}".format(dbd.cell(row=row_to_compare, column=column_to_compare).coordinate,ws.cell(row=row_comparing, column=column_comparing).coordinate)

# Method for setting function AVERAGE for each query and COUNT of queries
def createAVGandCOUNT(ws1,column_start):
        for i in range (0,4):    
                ws1['{0}'.format(ws1.cell(row=9, column=column_start+i).coordinate)] = "=AVERAGE({0}:{1})".format(ws1.cell(row=101, column=column_start+3+i).coordinate,ws1.cell(row=2000, column=column_start+3+i).coordinate)
        ws1['{0}'.format(ws1.cell(row=9, column=column_start+4).coordinate)] = "=COUNT({0}:{1})".format(ws1.cell(row=101, column=column_start+3).coordinate,ws1.cell(row=2000, column=column_start+3).coordinate)
      
        
# Method for creating average table menu and table where the data are stored + formatting
def createAVGTable(ws1,column_start):
	# Average - line
	ws1.cell(row=8, column=column_start, value="query_duration_us")
	ws1.cell(row=8, column=column_start+1, value="resource_request_execution_ms")
	ws1.cell(row=8, column=column_start+2, value="used_memory_kb")
	ws1.cell(row=8, column=column_start+3, value="CPU_TIME")
	ws1.cell(row=8, column=column_start+4, value="queries_COUNT")
    	# Formatting - blue color and bold 
    	for cellColumn in range(column_start,column_start+5):
        	ws1.cell(row=8,column=cellColumn).fill=blueFill
         	ws1.cell(row=8,column=cellColumn).font=bold
            
        # Formatting average table - data - orange fill
        for cellColumn in range(column_start,column_start+5):
            if ws1.title == "DBD":
        	       ws1.cell(row=9,column=cellColumn).fill=orangeFill
            
	# Items - line
    	ws1.cell(row=99, column=column_start, value=0)    
	ws1.cell(row=100, column=column_start, value="start_timestamp")
	ws1.cell(row=100, column=column_start+1, value="transaction_id")
	ws1.cell(row=100, column=column_start+2, value="statement_id")
	ws1.cell(row=100, column=column_start+3, value="query_duration_us")
	ws1.cell(row=100, column=column_start+4, value="resource_request_execution_ms")
	ws1.cell(row=100, column=column_start+5, value="used_memory_kb")
	ws1.cell(row=100, column=column_start+6, value="CPU_TIME")
    	# Formatting of table where data are stored
    	for cellColumn in range(column_start,column_start+8):
        	ws1.cell(row=100,column=cellColumn).fill=yellowFill
            	ws1.cell(row=100,column=cellColumn).font=bold
        
# Method for creating Overview - Basic page - only Head and DBD
def createOverview(ws,queries,testname):
    	# Header
        ws.cell(row=1, column=1, value="Comparison - Projections of Vertica Database Design x Own projections")
    	ws.cell(row=1, column=1).font = bold36
    	
        # Testname
	ws.cell(row=2, column=1, value="Testname:")
	ws.cell(row=2, column=2, value=testname)
        ws.cell(row=2, column=2).font = bold22
        
        # Queries
	ws.cell(row=3, column=1, value="Queries:")
	i = 2
	for query in queries:
		ws.cell(row=3, column=i, value=query)
        	ws.cell(row=1, column=i).font = bold22
		i += 1

        # Number of schemas
    	ws.cell(row=4, column=1, value="Number of schemas:")
	ws.cell(row=4, column=2, value=1)  
        
        # Schema - DBD
	ws.cell(row=11, column=1, value="Schema:")
    	ws.cell(row=11, column=2, value="DBD")
    	ws.cell(row=11, column=2).font=bold36
    
        # Description - DBD
	ws.cell(row=11, column=7, value="Description:")
    
        # Copying AVG table from DBD schema
        #for part in range(1,len(queries)+2):
                # columns
        for i in range (1,6):
                column_one = i
                for row_one in range (8,10):                                
                        ws['{0}'.format(ws.cell(row=row_one+4, column=column_one).coordinate)] = "=DBD!{0}".format(ws.cell(row=row_one, column=column_one).coordinate)
                        if row_one == 8:
                        	   ws.cell(row=row_one+4,column=column_one).fill=blueFill
         	                   ws.cell(row=row_one+4,column=column_one).font=bold
                        if row_one == 9:
                        	   ws.cell(row=row_one+4,column=column_one).fill=orangeFill
    
	# Width of cells    
	dims = {}
	for row in ws.rows:
		for cell in row:
			if cell.value:
				dims[cell.column] = max((dims.get(cell.column, 0), len(str(cell.value))))
	for col, value in dims.items():
		ws.column_dimensions[col].width = value    
        
# Method for adding new schema to Overview
def addToOverview(wb,ws,new,queries,schema):  
        # DBD schema - for comparing
    	dbd = wb['DBD']
    	# For appropriate number of queries (>1 query >>> 1 more table)    
	for part in range(1,len(queries)+2):
        # There is 5 columns: time,time,used memory, cpu, count of queries
		for i in range (1,6):
            		row_start = 21 + (int(ws.cell(row=4,column=2).value)-1)*10
			column_one = (part-1)*10 + i
                        # Schema and Description
	        	ws.cell(row=row_start, column=1, value="Schema:")
    	    		ws.cell(row=row_start, column=2, value=schema)
            		ws.cell(row=row_start, column=2).font=bold36
    
    		        # Description
	       		ws.cell(row=row_start, column=4, value="Description:")
            		# Copying data
			for j in range (0,3):
				ws['{0}'.format(ws.cell(row=row_start+j+1, column=column_one).coordinate)] = "={0}!{1}".format(schema,ws.cell(row=8+j, column=column_one).coordinate)
				if j == 0:
					ws.cell(row=row_start+j+1,column=column_one).fill=blueFill
					ws.cell(row=row_start+j+1,column=column_one).font=bold
				if j == 1:
					# Formatting - green/red 
					formatRedGreenFill(ws,dbd,row_start+j+1,column_one,8+j,column_one)
				

		# Formatting average table - green/red - in Pattern sheet
#		for i in range(1,5):
#			formatRedGreenFill(pattern,ws1,9,((part-1)*10 + i),14,((part-1)*10 + i))

#		for i in range (1,5):
#			formatDifference(pattern,ws1,9,((part-1)*10+i),9,((part-1)*10+i))

#		if len(queries) == 1:
#			break

#		if len(queries) > 1 and part == 1:
#			continue

		# USED BYTES PROJECTIONS
#		for j in range(1,10):
#			formatRedGreenFill(pattern,ws1,14,((part-1)*10+j),14,((part-1)*10+j))
#			formatDifference(pattern,ws1,14,((part-1)*10+j),14,((part-1)*10+j))       
		# Formatting - green/red 
 	                #if i < 5:
                     #   	formatRedGreenFill(ws,dbd,(row_start+2),(column_one),(row_start+2),column_one)
        	        	#ws.conditional_formatting.add('{0}'.format(ws.cell(row=row_start+2, column=column_one).coordinate), CellIsRule(operator='greaterThan', formula=['DBD!${0}'.format(dbd.cell(row=9, column=column_one).coordinate)], stopIfTrue=True, fill=redFill))
                		#ws.conditional_formatting.add('{0}'.format(ws.cell(row=row_start+2, column=column_one).coordinate), CellIsRule(operator='lessThan', formula=['DBD!${0}'.format(dbd.cell(row=9, column=column_one).coordinate)], stopIfTrue=True, fill=greenFill))                


def createProfile(ws1,column_start):
        # Query profile
	ws1.cell(row=17, column=column_start, value="Query profile:")
        ws1.cell(row=17,column=column_start).fill=blueFill
        ws1.cell(row=17,column=column_start+1).fill=blueFill
        ws1.cell(row=17,column=column_start).font=bold22        

	# Query profile - line
	ws1.cell(row=18, column=column_start, value="running_time")
	ws1.cell(row=18, column=column_start+1, value="memory_allocated_bytes")
	ws1.cell(row=18, column=column_start+2, value="read_from_disk_bytes")
	ws1.cell(row=18, column=column_start+3, value="path_line")    
 	for cellColumn in range(column_start,column_start+5):
        	ws1.cell(row=18,column=cellColumn).fill=blueFill
         	ws1.cell(row=18,column=cellColumn).font=bold           
  
        # Size of projections
	ws1.cell(row=12, column=column_start, value="Projection - Bytes:")
        ws1.cell(row=12,column=column_start).fill=lightblueFill    
        ws1.cell(row=12,column=column_start).font=bold
        i = 0
        for name in ["Customer:","Lineitem:","Nation:","Orders:","Part:","Partsupp:","Region:","Supplier:","SUM:"]:
                ws1.cell(row=13,column=column_start+i, value=name)
                ws1.cell(row=13,column=column_start+i).fill=lightblueFill
                ws1.cell(row=14,column=column_start+i).fill=greyFill
                i += 1

        ws1.cell(row=13,column=column_start+8).font=bold
        ws1['{0}'.format(ws1.cell(row=14, column=column_start+8).coordinate)] = "=SUM({0}:{1})".format(ws1.cell(row=14, column=column_start).coordinate,ws1.cell(row=14, column=column_start+7).coordinate)

def loadDataToExcelToParticularTable(row,ws,start_column):
	for i in range (1,9):
    		# integer data type, 1.column is schema - not storing in Excel file
		if i in [4,5,6,7]:
			ws['{0}'.format(ws.cell(row=101+ws.cell(row=99,column=start_column).value, column=start_column+i-1).coordinate)] = int(row[i])
    		# other data type
		else:   
			ws['{0}'.format(ws.cell(row=101+ws.cell(row=99,column=start_column).value, column=start_column+i-1).coordinate)] = row[i]    
        ws.cell(row=99,column=start_column).value += 1
    
def loadDataToExcel(rows,query,schema,testname,queries):
        # Opening excel - must be created and sheet with specific schema must be created
        wb = load_workbook('CompareOutput/{0}.xlsx'.format(testname))
        ws = wb[schema]
	for row in rows:
        	start_column = 1
            	#8 columns to store
            	loadDataToExcelToParticularTable(row,ws,start_column)
        	## increasing number of queries
		ws.cell(row=99,column=start_column).value += 1
		
        	# If there is more than 1 query, data are stored also in particular query table
		if len(queries)>1:
	                index = queries.index(query)
			start_column_query= 10*(index+1) + 1
			loadDataToExcelToParticularTable(row,ws,start_column_query)
			ws.cell(row=99,column=start_column_query).value += 1				    
        wb.save('CompareOutput/' + testname + '.xlsx')

# Method for creating new sheer according to new schema
# Particular step: duplicate Pattern sheet and fill Schema name
def duplicatePattern(schema,testname,queries,rows,query):
    wb = load_workbook('CompareOutput/{0}.xlsx'.format(testname))
    ws = wb["DBD"]
    overview = wb["Overview"] 
    pattern = wb["Pattern"]    
    # Creating new sheet
    if schema not in wb.sheetnames:
        new = wb.copy_worksheet(pattern)
        new.cell(row=3, column=2, value=schema)
        new.title = schema
        addToOverview(wb,overview,new,queries,schema)
        overview.cell(row=4,column=2).value = int(overview.cell(row=4,column=2).value) + 1 

	for part in range(1,len(queries)+2):
		for i in range(1,5):
			formatRedGreenFill(new,ws,9,((part-1)*10 + i),14,((part-1)*10 + i))

		for i in range (1,5):
			formatDifference(new,ws,9,((part-1)*10+i),9,((part-1)*10+i))

		if len(queries) == 1:
			break

		if len(queries) > 1 and part == 1:
			continue

		# USED BYTES PROJECTIONS
		for j in range(1,10):
			formatRedGreenFill(new,ws,14,((part-1)*10+j),14,((part-1)*10+j))
			formatDifference(new,ws,14,((part-1)*10+j),14,((part-1)*10+j))	

	wb.save('CompareOutput/' + testname + '.xlsx')        

# Method for loading Query Profile Path into the excel file        
def loadProfilePath(schema,testname,rows,queries,query):
	wb = load_workbook('CompareOutput/{0}.xlsx'.format(testname))
    	ws = wb[schema]	
        # NEROZLISUJE SE KOLIK JE QUERY!!!                
        for i in range(1,len(queries)+2):
        	if len(queries) == 1:
            		start_column= 1
            	if len(queries) > 1 and i == 1:
                	continue
            	if i > 1:                
                	start_column= 10*(i+1) + 1        	
                	#if ws.cell(row=5,column=start_column+1).value == query:
                if str(ws['{0}'.format(ws.cell(row=5,column=start_column+1).coordinate)]) == str(query):
			tmp_row = 0
			for row in rows:
				tmp_column = 0
                		print "TEEEEEEEEEST"
				for item in row:
					print item				
					#ws['{0}'.format(ws.cell(row=19+tmp_row,column=start_column+tmp_column).coordinate)]=str(item)
					ws.cell(row=19+tmp_row,column=start_column+tmp_column,value=item)
					tmp_column += 1
				tmp_row += 1
         
def formatQueryProfilePlan(ws1):  
	dxf = DifferentialStyle(fill=yellowFill)
	rule = Rule(type="containsText", operator="containsText", text="> JOIN", dxf=dxf)
	rule.formula = ['NOT(ISERROR(SEARCH("> JOIN",A19)))']
	ws1.conditional_formatting.add('A19:ZZ99', rule)

	dxf = DifferentialStyle(fill=lightblueFill)
	rule = Rule(type="containsText", operator="containsText", text="Filter", dxf=dxf)
	rule.formula = ['NOT(ISERROR(SEARCH("Filter",A19)))']
	ws1.conditional_formatting.add('A19:ZZ99', rule)       
	
	dxf = DifferentialStyle(fill=orangeFill)
	rule = Rule(type="containsText", operator="containsText", text="Join Cond", dxf=dxf)
	rule.formula = ['NOT(ISERROR(SEARCH("Join Cond",A19)))']
	ws1.conditional_formatting.add('A19:ZZ99', rule)
	
	dxf = DifferentialStyle(fill=pinkFill)
	rule = Rule(type="containsText", operator="containsText", text="Projection:", dxf=dxf)
	rule.formula = ['NOT(ISERROR(SEARCH("Projection:",A16)))']
	ws1.conditional_formatting.add('A19:ZZ99', rule)
	
	dxf = DifferentialStyle(fill=lightgreenFill)
	rule = Rule(type="containsText", operator="containsText", text="SELECT", dxf=dxf)
	rule.formula = ['NOT(ISERROR(SEARCH("SELECT",A19)))']
	ws1.conditional_formatting.add('A19:ZZ99', rule)
	
	dxf = DifferentialStyle(fill=darkredFill)
	rule = Rule(type="containsText", operator="containsText", text="SORT [", dxf=dxf)
	rule.formula = ['NOT(ISERROR(SEARCH("SORT [",A19)))']
	ws1.conditional_formatting.add('A19:ZZ99', rule)
	
	dxf = DifferentialStyle(fill=redFill)
	rule = Rule(type="containsText", operator="containsText", text="> GROUPBY", dxf=dxf)
	rule.formula = ['NOT(ISERROR(SEARCH("> GROUPBY",A19)))']
	ws1.conditional_formatting.add('A19:ZZ99', rule)
	
	dxf = DifferentialStyle(fill=blueFill)
	rule = Rule(type="containsText", operator="containsText", text="Outer -> STORAGE", dxf=dxf)
	rule.formula = ['NOT(ISERROR(SEARCH("Outer -> STORAGE",A19)))']
	ws1.conditional_formatting.add('A19:ZZ99', rule)
	
	dxf = DifferentialStyle(fill=greenFill)
	rule = Rule(type="containsText", operator="containsText", text="Inner -> STORAGE", dxf=dxf)
	rule.formula = ['NOT(ISERROR(SEARCH("Inner -> STORAGE",A19)))']
	ws1.conditional_formatting.add('A19:ZZ99', rule)
	# end 	
	
	return ws1
  
# Method for creating Excel file if the file is not created already
def createExcelFile(testname,queries):
    	if not os.path.exists('./CompareOutput/' + testname + '.xlsx'):
		# Create workbook and sheets
		wb = Workbook()
		ws = wb.active
        	# There is 2 sheets - Overview (dashboard) and DBD
		ws1 = wb.create_sheet("DBD")
		ws.title = "Overview"

		# Header
		    # Testname
		ws1.cell(row=1, column=1, value="Testname:")
		ws1.cell(row=1, column=2, value=testname)
		ws1.cell(row=1, column=2).font = bold22
		
		    # Queries
		ws1.cell(row=2, column=1, value="Queries:")
		i = 2
		for query in queries:
			ws1.cell(row=2, column=i, value=query)
			ws1.cell(row=1, column=i).font = bold22
			i += 1
		    # Schema and Description
		ws1.cell(row=3, column=1, value="Schema:")
		ws1.cell(row=3, column=2).font=bold36
	    
		    # Description
		ws1.cell(row=4, column=1, value="Description:")
	    
		    # Overview
		if len(queries)>1:
			ws1.cell(row=5, column=1, value="OVERVIEW")
			ws1.cell(row=5, column=1).fill=yellowFill
			ws1.cell(row=5, column=1).font=bold22

		# Table lines   
		tmp = 0
		for part in range(1,len(queries)+2):
			createAVGTable(ws1,(part-1)*10 + 1)
			createAVGandCOUNT(ws1,(part-1)*10 + 1)
			if len(queries) == 1:
				createProfile(ws1,1)
				break			                   
			if part > 1:
				createProfile(ws1,(part-1)*10 + 1)                        
				ws1.cell(row=5,column=(part-1)*10 + 1,value="Query: ")
				ws1.cell(row=5,column=(part-1)*10 + 2,value=str(queries[part-2]))
				ws1.cell(row=5,column=(part-1)*10 + 2).font=bold22
			
        	# Setting format for Query Profile Plan part of Excel file    
		ws1 = formatQueryProfilePlan(ws1)				    
	
		# Width of cells
		dims = {}
		for row in ws1.rows:
			for cell in row:
				if cell.value:
					dims[cell.column] = max((dims.get(cell.column, 0), len(str(cell.value))))
		for col, value in dims.items():
			ws1.column_dimensions[col].width = value

            
		# Create pattern for other schemas
		pattern = wb.copy_worksheet(ws1)
		pattern.title = "Pattern"
        
        	# In DBD sheet set schema name to DBD
		ws1.cell(row=3, column=2, value="DBD")
	    
		# Formatting average table - green/red - in Pattern sheet
		for part in range(1,len(queries)+2):			
            		for i in range(1,5):
                            	formatRedGreenFill(pattern,ws1,9,((part-1)*10 + i),14,((part-1)*10 + i))
			
			for i in range (1,5):
                		formatDifference(pattern,ws1,9,((part-1)*10+i),9,((part-1)*10+i))
			    
			if len(queries) == 1:
				break
				
			if len(queries) > 1 and part == 1:
				continue
			
			# USED BYTES PROJECTIONS
            		for j in range(1,10):
                            	formatRedGreenFill(pattern,ws1,14,((part-1)*10+j),14,((part-1)*10+j))
                    		formatDifference(pattern,ws1,14,((part-1)*10+j),14,((part-1)*10+j))

        	# Method for creating Overview        
		createOverview(ws,queries,testname) 
 
		wb.save('CompareOutput/' + testname + '.xlsx')
	    
