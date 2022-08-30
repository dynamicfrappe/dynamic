# Copyright (c) 2022, Dynamic and contributors
# For license information, please see license.txt

from pty import slave_open
import frappe
from frappe.model.document import Document
import calendar
from frappe.utils import today
class SalesPersonCommetion(Document):
	def set_messing_dates(self):
		if self.date :
			#self.to_date = today
			date_list = str(self.date).split('-')
			year_name = date_list[0]
			month_name = date_list[1]
			self.from_date  = f"""{year_name}-{month_name}-01"""
			self.to_date= f"""{year_name}-{month_name}-{calendar.monthrange(int(year_name), int(month_name))[1]}"""


	#caculate item group qty / amount in range from date to to date values	
	def caculate_qty_amount(self):
		if self.date :
			caculation_sql =  frappe.db.sql( f""" SELECT 
								SUM(`tabSales Invoice Item`.amount) as amount ,
								SUM(`tabSales Invoice Item`.qty) as qty
								FROM 
								`tabSales Invoice` INNER JOIN 
								`tabSales Invoice Item`
								ON `tabSales Invoice`.name = `tabSales Invoice Item`.parent
								WHERE `tabSales Invoice`.name in 
								(SELECT parent FROM `tabSales Team` 
								WHERE sales_person = '{self.sales_person}')
								AND `tabSales Invoice`.docstatus = 1 and
								`tabSales Invoice Item`.item_group = '{self.item__group}' and 
								`tabSales Invoice`.posting_date between '{self.from_date }'
								and '{self.to_date}' 
							""" ,as_dict =1)
			#frappe.throw(str(caculation_sql))
			if caculation_sql and len (caculation_sql) > 0 :
				total_amount =  float(caculation_sql[0].get("amount") or 0) + float(self.invocie_amount or 0)
				totat_qty = float(caculation_sql[0].get("qty") or 0) + float(self.invoice_qty or 0 )
				# frappe.throw(str(totat_qty))
				#get Template Rate and Amount
				amount = total_amount if self.base_on == "Amount" else totat_qty
				template_rate =frappe.db.sql(f""" 
				SELECT commission_amount as amount , commission_rate as rate 
				FROM `tabCommission Template Child` WHERE parent = '{self.commission_template}'
				AND amount_from < {amount}
				""",as_dict =1)
				# frappe.throw(str(template_rate))
				# seq = [x['the_key'] for x in template_rate]
				if template_rate and len(template_rate) > 0 :
					self.commission_percent = max([float(x.get('rate') or 0)  for x in template_rate])
					self.commission_amount = max([float(x.get('amount') or 0)for x in template_rate])
				percent_factor = self.invoice_qty if self.base_on == "Qty" else  self.invocie_amount
				main_amount = float(self.commission_amount or 0) if float(self.commission_amount or 0)> 0 else float(self.commission_percent or 0)  *percent_factor
				if self.base_on == "Qty":
					main_amount = float(main_amount or 0) * float(self.invoice_qty or 0)
				# frappe.throw(str(template_rate))
				self.amount = main_amount
	#update monyhlu commetion base on date and item group 
	def update_monthly_commetions(self):
		pass
	def validate_invocie_status(self):
		invocie = frappe.get_doc("Sales Invoice" , self.invocie).docstatus
		if invocie == 1 :
			self.update_monthly_commetions()
	def validate(self):
		self.set_messing_dates()
		self.caculate_qty_amount()
		self.validate_invocie_status()
