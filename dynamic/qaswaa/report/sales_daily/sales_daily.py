# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

# import frappe


def execute(filters=None):
	columns, data = [], []
	return columns, data
def get_data(filters):
	sql = '''
		SELECT 
			posting_date , name , set_warehouse , customer ,
			base_total , base_total_taxes_and_charges , base_grand_total ,
			
		'''
