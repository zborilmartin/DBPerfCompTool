#!/usr/bin/env python
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font, Color,PatternFill
from openpyxl.styles import colors
from openpyxl.formatting.rule import ColorScaleRule, CellIsRule, FormulaRule
from openpyxl.styles.differential import DifferentialStyle
from openpyxl.formatting import Rule
from openpyxl import load_workbook    

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

        
    
def createAVGTable(ws1,column_start):
	       # Average - line
	ws1.cell(row=8, column=column_start, value="query_duration_us")
	ws1.cell(row=8, column=column_start+1, value="resource_request_execution_ms")
	ws1.cell(row=8, column=column_start+2, value="used_memory_kb")
	ws1.cell(row=8, column=column_start+3, value="CPU_TIME")
	ws1.cell(row=8, column=column_start+4, value="queries_COUNT")
    	for cellColumn in range(column_start,column_start+5):
        	ws1.cell(row=8,column=cellColumn).fill=blueFill
         	ws1.cell(row=8,column=cellColumn).font=bold
            
            # Formatting average table - DBD 
        for cellColumn in range(column_start,column_start+5):
        	ws1.cell(row=9,column=cellColumn).fill=orangeFill
            
	       # Items - line
	ws1.cell(row=100, column=column_start, value="start_timestamp")
	ws1.cell(row=100, column=column_start+1, value="transaction_id")
	ws1.cell(row=100, column=column_start+2, value="statement_id")
	ws1.cell(row=100, column=column_start+3, value="query_duration_us")
	ws1.cell(row=100, column=column_start+4, value="resource_request_execution_ms")
	ws1.cell(row=100, column=column_start+5, value="used_memory_kb")
	ws1.cell(row=100, column=column_start+6, value="CPU_TIME")
    	for cellColumn in range(column_start,column_start+8):
        	ws1.cell(row=100,column=cellColumn).fill=yellowFill
            	ws1.cell(row=100,column=cellColumn).font=bold
        
	ws1.cell(row=10, column=column_start, value="Projection - Bytes:")
        ws1.cell(row=10,column=column_start).fill=lightblueFill    
        ws1.cell(row=10,column=column_start).font=bold
    	ws1.cell(row=11, column=column_start, value="Customer:")
        ws1.cell(row=11,column=column_start).fill=lightblueFill
        ws1.cell(row=12,column=column_start).fill=greyFill
    	ws1.cell(row=11, column=column_start+1, value="Lineitem:")
        ws1.cell(row=11,column=column_start+1).fill=lightblueFill    
        ws1.cell(row=12,column=column_start+1).fill=greyFill      
    	ws1.cell(row=11, column=column_start+2, value="Nation:")
        ws1.cell(row=11,column=column_start+2).fill=lightblueFill    
        ws1.cell(row=12,column=column_start+2).fill=greyFill    
    	ws1.cell(row=11, column=column_start+3, value="Orders:")
        ws1.cell(row=11,column=column_start+3).fill=lightblueFill    
        ws1.cell(row=12,column=column_start+3).fill=greyFill    
    	ws1.cell(row=11, column=column_start+4, value="Part:")
        ws1.cell(row=11,column=column_start+4).fill=lightblueFill    
        ws1.cell(row=12,column=column_start+4).fill=greyFill    
    	ws1.cell(row=11, column=column_start+5, value="Partsupp:")
        ws1.cell(row=11,column=column_start+5).fill=lightblueFill    
        ws1.cell(row=12,column=column_start+5).fill=greyFill    
    	ws1.cell(row=11, column=column_start+6, value="Region:")
        ws1.cell(row=11,column=column_start+6).fill=lightblueFill    
        ws1.cell(row=12,column=column_start+6).fill=greyFill    
    	ws1.cell(row=11, column=column_start+7, value="Supplier:")
        ws1.cell(row=11,column=column_start+7).fill=lightblueFill    
        ws1.cell(row=12,column=column_start+7).fill=greyFill            
        

def createProfile(ws1,column_start):
            # Memory used
	#ws1.cell(row=11, column=column_start, value="Memory used:")
        #ws1.cell(row=11,column=column_start).fill=blueFill
        #ws1.cell(row=11,column=column_start).font=bold
        #ws1.cell(row=11,column=column_start+1).fill=orangeFill
        
            # Query profile
	ws1.cell(row=13, column=column_start, value="Query profile:")
        ws1.cell(row=13,column=column_start).fill=blueFill
        ws1.cell(row=13,column=column_start+1).fill=blueFill
        ws1.cell(row=13,column=column_start).font=bold22        

	       # Query profile - line
	ws1.cell(row=14, column=column_start, value="running_time")
	ws1.cell(row=14, column=column_start+1, value="memory_allocated_bytes")
	ws1.cell(row=14, column=column_start+2, value="read_from_disk_bytes")
	ws1.cell(row=14, column=column_start+3, value="path_line")    
 	for cellColumn in range(column_start,column_start+5):
        	ws1.cell(row=14,column=cellColumn).fill=blueFill
         	ws1.cell(row=14,column=cellColumn).font=bold           
        
def createExcelFile(testname,queries):
    
        
        # Create workbook and sheets
	wb = Workbook()
	ws = wb.active
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
                if len(queries) == 1:
                        createProfile(ws1,1)
                        break
                #if len(queries) > 1 and part:                    
                if part > 1:
                        createProfile(ws1,(part-1)*10 + 1)
                        ws1.cell(row=5,column=(part-1)*10 + 1,value="Query: "+str(queries[part-2]))
                        ws1.cell(row=5,column=(part-1)*10 + 1).font=bold22
            	
        # Formating Query Profile Plan part
        
        dxf = DifferentialStyle(fill=yellowFill)
        rule = Rule(type="containsText", operator="containsText", text="> JOIN", dxf=dxf)
        rule.formula = ['NOT(ISERROR(SEARCH("> JOIN",A15)))']
        ws1.conditional_formatting.add('A15:ZZ99', rule)
        
        dxf = DifferentialStyle(fill=lightblueFill)
        rule = Rule(type="containsText", operator="containsText", text="Filter", dxf=dxf)
        rule.formula = ['NOT(ISERROR(SEARCH("Filter",A15)))']
        ws1.conditional_formatting.add('A15:ZZ99', rule)       
        
        dxf = DifferentialStyle(fill=orangeFill)
        rule = Rule(type="containsText", operator="containsText", text="Join Cond", dxf=dxf)
        rule.formula = ['NOT(ISERROR(SEARCH("Join Cond",A15)))']
        ws1.conditional_formatting.add('A15:ZZ99', rule)
        
        dxf = DifferentialStyle(fill=pinkFill)
        rule = Rule(type="containsText", operator="containsText", text="Projection:", dxf=dxf)
        #rule.formula = ['NOT(ISERROR(SEARCH("Projection:",A16)))']
        ws1.conditional_formatting.add('A15:ZZ99', rule)
        
        dxf = DifferentialStyle(fill=lightgreenFill)
        rule = Rule(type="containsText", operator="containsText", text="SELECT", dxf=dxf)
        rule.formula = ['NOT(ISERROR(SEARCH("SELECT",A15)))']
        ws1.conditional_formatting.add('A15:ZZ99', rule)
        
        dxf = DifferentialStyle(fill=darkredFill)
        rule = Rule(type="containsText", operator="containsText", text="SORT [", dxf=dxf)
        rule.formula = ['NOT(ISERROR(SEARCH("SORT [",A15)))']
        ws1.conditional_formatting.add('A15:ZZ99', rule)
        
        dxf = DifferentialStyle(fill=redFill)
        rule = Rule(type="containsText", operator="containsText", text="> GROUPBY", dxf=dxf)
        rule.formula = ['NOT(ISERROR(SEARCH("> GROUPBY",A15)))']
        ws1.conditional_formatting.add('A15:ZZ99', rule)
        
        dxf = DifferentialStyle(fill=blueFill)
        rule = Rule(type="containsText", operator="containsText", text="Outer -> STORAGE", dxf=dxf)
        rule.formula = ['NOT(ISERROR(SEARCH("Outer -> STORAGE",A15)))']
        ws1.conditional_formatting.add('A15:ZZ99', rule)
        
        dxf = DifferentialStyle(fill=greenFill)
        rule = Rule(type="containsText", operator="containsText", text="Inner -> STORAGE", dxf=dxf)
        rule.formula = ['NOT(ISERROR(SEARCH("Inner -> STORAGE",A15)))']
        ws1.conditional_formatting.add('A15:ZZ99', rule)
        # end 
        
        
                                    
        
    	# Width of cells
	dims = {}
	for row in ws1.rows:
		for cell in row:
			if cell.value:
				dims[cell.column] = max((dims.get(cell.column, 0), len(cell.value)))
	for col, value in dims.items():
		ws1.column_dimensions[col].width = value

        # Create pattern
	pattern = wb.copy_worksheet(ws1)
    	ws1.cell(row=3, column=2, value="DBD")

    
        # Formatting average table - green/red - PATTERN
        for part in range(1,len(queries)+2):
                #if len(queries) > 1 and part:                            
                pattern.conditional_formatting.add('{0}'.format(ws1.cell(row=9, column=(part-1)*10 + 1).coordinate), CellIsRule(operator='greaterThan', formula=['DBD!${0}'.format(ws1.cell(row=9, column=(part-1)*10 + 1).coordinate)], stopIfTrue=True, fill=redFill))
                pattern.conditional_formatting.add('{0}'.format(ws1.cell(row=9, column=(part-1)*10 + 1).coordinate), CellIsRule(operator='lessThan', formula=['DBD!${0}'.format(ws1.cell(row=9, column=(part-1)*10 + 1).coordinate)], stopIfTrue=True, fill=greenFill))
                pattern.conditional_formatting.add('{0}'.format(ws1.cell(row=9, column=(part-1)*10 + 2).coordinate), CellIsRule(operator='greaterThan', formula=['DBD!${0}'.format(ws1.cell(row=9, column=(part-1)*10 + 2).coordinate)], stopIfTrue=True, fill=redFill))
                pattern.conditional_formatting.add('{0}'.format(ws1.cell(row=9, column=(part-1)*10 + 2).coordinate), CellIsRule(operator='lessThan', formula=['DBD!${0}'.format(ws1.cell(row=9, column=(part-1)*10 + 2).coordinate)], stopIfTrue=True, fill=greenFill))
                pattern.conditional_formatting.add('{0}'.format(ws1.cell(row=9, column=(part-1)*10 + 3).coordinate), CellIsRule(operator='greaterThan', formula=['DBD!${0}'.format(ws1.cell(row=9, column=(part-1)*10 + 3).coordinate)], stopIfTrue=True, fill=redFill))
                pattern.conditional_formatting.add('{0}'.format(ws1.cell(row=9, column=(part-1)*10 + 3).coordinate), CellIsRule(operator='lessThan', formula=['DBD!${0}'.format(ws1.cell(row=9, column=(part-1)*10 + 3).coordinate)], stopIfTrue=True, fill=greenFill))
                pattern.conditional_formatting.add('{0}'.format(ws1.cell(row=9, column=(part-1)*10 + 4).coordinate), CellIsRule(operator='greaterThan', formula=['DBD!${0}'.format(ws1.cell(row=9, column=(part-1)*10 + 4).coordinate)], stopIfTrue=True, fill=redFill))
                pattern.conditional_formatting.add('{0}'.format(ws1.cell(row=9, column=(part-1)*10 + 4).coordinate), CellIsRule(operator='lessThan', formula=['DBD!${0}'.format(ws1.cell(row=9, column=(part-1)*10 + 4).coordinate)], stopIfTrue=True, fill=greenFill))
                
                pattern.conditional_formatting.add('{0}'.format(ws1.cell(row=11, column=(part-1)*10 + 2).coordinate), CellIsRule(operator='lessThan', formula=['DBD!${0}'.format(ws1.cell(row=11, column=(part-1)*10 + 2).coordinate)], stopIfTrue=True, fill=greenFill))
                pattern.conditional_formatting.add('{0}'.format(ws1.cell(row=11, column=(part-1)*10 + 2).coordinate), CellIsRule(operator='greaterThan', formula=['DBD!${0}'.format(ws1.cell(row=11, column=(part-1)*10 + 2).coordinate)], stopIfTrue=True, fill=redFill))
                if len(queries) == 1:
                        break

        
        
        

            
        
                
    
	
    	
    
	wb.save('CompareOutput' + testname + '.xlsx')
