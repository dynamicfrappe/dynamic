# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import frappe
from frappe import _, scrub
from frappe.utils import add_days, add_to_date, flt, getdate
from six import iteritems

from erpnext.accounts.utils import get_fiscal_year


def execute(filters=None):
	return Analytics(filters).run()


class Analytics(object):
	def __init__(self, filters=None):
		self.filters = frappe._dict(filters or {})
		self.date_field = "transaction_date"
		# self.date_field = (
		# 	"transaction_date"
		# 	if self.filters.doc_type in ["Sales Order", "Purchase Order"]
		# 	else "posting_date"
		# )
		self.months = [
			"Jan",
			"Feb",
			"Mar",
			"Apr",
			"May",
			"Jun",
			"Jul",
			"Aug",
			"Sep",
			"Oct",
			"Nov",
			"Dec",
		]
		self.get_period_date_ranges()

	def run(self):
		self.get_columns()
		self.get_data()
		self.get_chart_data()

		# Skipping total row for tree-view reports
		skip_total_row = 0

		# if self.filters.tree_type in ["Supplier Group", "Item Group", "Customer Group", "Territory"]:
		# 	skip_total_row = 1 self.chart

		return self.columns, self.data, None, self.chart, None, skip_total_row

	def get_columns(self):
		self.columns = [
			{
				"label": _("Year	"),#self.filters.tree_type
				"options": self.filters.tree_type if self.filters.tree_type != "Order Type" else "",
				"fieldname": "entity",
				"fieldtype": "Link" if self.filters.tree_type != "Order Type" else "Data",
				"width": 140 if self.filters.tree_type != "Order Type" else 200,
			}
		]
		# if self.filters.tree_type in ["Customer", "Supplier", "Item"]:
		# 	self.columns.append(
				
		# 		{
		# 			"label": _(self.filters.tree_type + " Name_xxx"),
		# 			"fieldname": "entity_name",
		# 			"fieldtype": "Data",
		# 			"width": 140,
		# 		}
		# 	)
			
		# if self.filters.tree_type == "Item":
		# 	self.columns.append(
		# 		{
		# 			"label": _("UOM"),
		# 			"fieldname": "stock_uom",
		# 			"fieldtype": "Link",
		# 			"options": "UOM",
		# 			"width": 100,
		# 		}
		# 	)
			
		# if self.filters.tree_type == "Warehouse":
		# 	self.columns.append(
		# 		{
		# 			"label": _("Warehouse"),
		# 			"fieldname": "warehouse",
		# 			"fieldtype": "Link",
		# 			"options":"Warehouse",
		# 			"width": 140,
		# 		}
		# 	)
		for end_date in self.periodic_daterange:
			period = self.get_period(end_date)
			self.columns.append(
				{"label": _(period), "fieldname": scrub(period), "fieldtype": "Float", "width": 120}
			)

		self.columns.append(
			{"label": _("Total"), "fieldname": "total", "fieldtype": "Float", "width": 120}
		)

	def get_data(self):
		
		self.get_data_quotation()
		self.get_rows()
		# if self.filters.tree_type in ["Customer", "Supplier"]:
		# 	self.get_sales_transactions_based_on_customers_or_suppliers()
		# 	self.get_rows()

		# elif self.filters.tree_type == "Item":
		# 	self.get_sales_transactions_based_on_items()
		# 	self.get_rows()

		# elif self.filters.tree_type == "Warehouse":
		# 	self.get_sales_transactions_based_on_warehouse()
		# 	self.get_rows()

		# elif self.filters.tree_type in ["Customer Group", "Supplier Group", "Territory"]:
		# 	self.get_sales_transactions_based_on_customer_or_territory_group()
		# 	self.get_rows_by_group()

		# elif self.filters.tree_type == "Item Group":
		# 	self.get_sales_transactions_based_on_item_group()
		# 	self.get_rows_by_group()

		# elif self.filters.tree_type == "Order Type":
		# 	if self.filters.doc_type != "Sales Order":
		# 		self.data = []
		# 		return
		# 	self.get_sales_transactions_based_on_order_type()
		# 	self.get_rows_by_group()

		# elif self.filters.tree_type == "Project":
		# 	self.get_sales_transactions_based_on_project()
		# 	self.get_rows()
	def get_data_quotation(self):
		condition = "WHERE 1=1 AND docstatus = 1 "
		if self.filters.get("orderd") == "Yes":
			condition += "AND status = '%s' "%("Ordered")
		if self.filters.get("from_date") and self.filters.get("to_date"):
			if(self.filters.get("from_date") > self.filters.get("to_date")):
				frappe.throw(_("From Date must be before To Date"))
			condition += "AND {date_field} between '{from_date}' and '{to_date}".format(date_field=self.date_field,from_date = self.filters.from_date, to_date = self.filters.to_date)


		sql = """SELECT name as entity,quotation_to,{date_field}, 1 as value_field  FROM `tabQuotation`
			{condition}'
		""".format(condition=condition,date_field=self.date_field)
		self.entries = frappe.db.sql(sql,as_dict=1)
		self.entity_names = {}
		for d in self.entries:
			self.entity_names.setdefault(d.name, d.quotation_to)

	def get_rows(self):
		self.data = []
		self.get_periodic_data()
		#self.entity_periodic_data--> {'Week 5 2023': {'qty': 2.0}, 'Week 6 2023': {'qty': 1.0}}
		# print('\n\n self.periodic_daterange-->',self.periodic_daterange)
		for entity, period_data in iteritems(self.entity_periodic_data):
			# print('\n\n ##&&& entity, period_data',entity, period_data)
			row = {
				"entity": entity,
				# "entity_name": self.entity_names.get(entity) if hasattr(self, "entity_names") else None,
			}

			# amount = flt(period_data.get('qty', 0.0))
			# row[scrub(entity)] = amount
			total = 0
			for end_date in self.periodic_daterange: #? total week
				period = self.get_period(end_date)
				# print(f'\n\n**period, \"{period}\",\n',type(period_data))
				if not period_data.get(period):
					period_data.update({period: {'qty':0}})
					# period_data['period'] = setdefault(year, frappe._dict())
				amount = flt(period_data.get(period,period).get('qty', 0.0))
				# print('\n\n end_date--period-->amount',end_date,period,amount)
				row[scrub(period)] = amount
				total += amount

			row["total"] = total

			if self.filters.tree_type == "Item":
				row["stock_uom"] = period_data.get("stock_uom")

			self.data.append(row)
		# print('\n\n **/// self.data.item-->',self.data,'\n\n')


	def get_periodic_data(self):
		self.entity_periodic_data = frappe._dict()
		print('\n\n self.entries-->',self.entries)
		#{'entity': 'SAL-QTN-2022-00005', 'quotation_to': 'Lead', 'date_field': datetime.date(2022, 12, 28), 'value_field': 1}
		for d in self.entries:
			if self.filters.tree_type == "Supplier Group":
				d.entity = self.parent_child_map.get(d.entity)
			#! change row data here
			year = (d.get(self.date_field)).isocalendar()[0]
			period = self.get_period(d.get(self.date_field))
			self.entity_periodic_data.setdefault(year, frappe._dict()).setdefault(period, frappe._dict()).setdefault('qty', 0.0)
			self.entity_periodic_data[year][period]['qty'] += flt(d.value_field)

			# self.entity_periodic_data.setdefault(d.entity, frappe._dict()).setdefault(period, 0.0)
			# self.entity_periodic_data[d.entity][period] += flt(d.value_field)

			if self.filters.tree_type == "Item":
				self.entity_periodic_data[d.entity]["stock_uom"] = d.stock_uom
		# print('\n\n---##$$$ self.entity_periodic_data-->',self.entity_periodic_data)

	def get_period(self, posting_date):
		# period = "Week " + str(posting_date.isocalendar()[1]) + " " + str(posting_date.year)
		if self.filters.range == "Weekly":
			period = "Week " + str(posting_date.isocalendar()[1]) + " " + str(posting_date.year)
		elif self.filters.range == "Monthly":
			period = str(self.months[posting_date.month - 1]) + " " + str(posting_date.year)
		elif self.filters.range == "Quarterly":
			period = "Quarter " + str(((posting_date.month - 1) // 3) + 1) + " " + str(posting_date.year)
		else:
			year = get_fiscal_year(posting_date, company=self.filters.company)
			period = str(year[0])
		return period

	def get_period_date_ranges(self):
		from dateutil.relativedelta import MO, relativedelta

		from_date, to_date = getdate(self.filters.from_date), getdate(self.filters.to_date)

		increment = {"Monthly": 1, "Quarterly": 3, "Half-Yearly": 6, "Yearly": 12}.get(
			self.filters.range, 1
		)

		if self.filters.range in ["Monthly", "Quarterly"]:
			from_date = from_date.replace(day=1)
		elif self.filters.range == "Yearly":
			from_date = get_fiscal_year(from_date)[1]
		else:
			from_date = from_date + relativedelta(from_date, weekday=MO(-1))

		self.periodic_daterange = []
		for dummy in range(1, 53):
			if self.filters.range == "Weekly":
				period_end_date = add_days(from_date, 6)
			else:
				period_end_date = add_to_date(from_date, months=increment, days=-1)

			if period_end_date > to_date:
				period_end_date = to_date

			self.periodic_daterange.append(period_end_date)

			from_date = add_days(period_end_date, 1)
			if period_end_date == to_date:
				break

	def get_chart_data(self):
		length = len(self.columns)

		labels = [d.get("label") for d in self.columns[1 : length - 1]]
		self.entries = self.data
		values = []
		if self.data:
			del self.data[0]['entity']
			del self.data[0]['total']
			for key,value in self.data[0].items():
				values.append(value)
		
		self.chart = {
			'data':{
			'labels':labels,
			'datasets':[
				{'name':'Count','values':values},
			]
		},
		'type':'bar'
		}
		self.chart["fieldtype"] = "Currency"

	# def get_groups(self):
	# 	if self.filters.tree_type == "Territory":
	# 		parent = "parent_territory"
	# 	if self.filters.tree_type == "Customer Group":
	# 		parent = "parent_customer_group"
	# 	if self.filters.tree_type == "Item Group":
	# 		parent = "parent_item_group"
	# 	if self.filters.tree_type == "Supplier Group":
	# 		parent = "parent_supplier_group"

	# 	self.depth_map = frappe._dict()

	# 	self.group_entries = frappe.db.sql(
	# 		"""select name, lft, rgt , {parent} as parent
	# 		from `tab{tree}` order by lft""".format(
	# 			tree=self.filters.tree_type, parent=parent
	# 		),
	# 		as_dict=1,
	# 	)

	# 	for d in self.group_entries:
	# 		if d.parent:
	# 			self.depth_map.setdefault(d.name, self.depth_map.get(d.parent) + 1)
	# 		else:
	# 			self.depth_map.setdefault(d.name, 0)

	# def get_teams(self):
	# 	self.depth_map = frappe._dict()

	# 	self.group_entries = frappe.db.sql(
	# 		""" select * from (select "Order Types" as name, 0 as lft,
	# 		2 as rgt, '' as parent union select distinct order_type as name, 1 as lft, 1 as rgt, "Order Types" as parent
	# 		from `tab{doctype}` where ifnull(order_type, '') != '') as b order by lft, name
	# 	""".format(
	# 			doctype=self.filters.doc_type
	# 		),
	# 		as_dict=1,
	# 	)

	# 	for d in self.group_entries:
	# 		if d.parent:
	# 			self.depth_map.setdefault(d.name, self.depth_map.get(d.parent) + 1)
	# 		else:
	# 			self.depth_map.setdefault(d.name, 0)

	# def get_supplier_parent_child_map(self):
	# 	self.parent_child_map = frappe._dict(
	# 		frappe.db.sql(""" select name, supplier_group from `tabSupplier`""")
	# 	)




	# def get_sales_transactions_based_on_order_type(self):
	# 	if self.filters["value_quantity"] == "Value":
	# 		value_field = "base_net_total"
	# 	else:
	# 		value_field = "total_qty"

	# 	self.entries = frappe.db.sql(
	# 		""" select s.order_type as entity, s.{value_field} as value_field, s.{date_field}
	# 		from `tab{doctype}` s where s.docstatus = 1 and s.company = %s and s.{date_field} between %s and %s
	# 		and ifnull(s.order_type, '') != '' order by s.order_type
	# 	""".format(
	# 			date_field=self.date_field, value_field=value_field, doctype=self.filters.doc_type
	# 		),
	# 		(self.filters.company, self.filters.from_date, self.filters.to_date),
	# 		as_dict=1,
	# 	)

	# 	self.get_teams()

	# def get_sales_transactions_based_on_customers_or_suppliers(self):
	# 	if self.filters["value_quantity"] == "Value":
	# 		value_field = "base_net_total as value_field"
	# 	else:
	# 		value_field = "total_qty as value_field"

	# 	if self.filters.tree_type == "Customer":
	# 		entity = "customer as entity"
	# 		entity_name = "customer_name as entity_name"
	# 	else:
	# 		entity = "supplier as entity"
	# 		entity_name = "supplier_name as entity_name"

	# 	self.entries = frappe.get_all(
	# 		self.filters.doc_type,
	# 		fields=[entity, entity_name, value_field, self.date_field],
	# 		filters={
	# 			"docstatus": 1,
	# 			"company": self.filters.company,
	# 			self.date_field: ("between", [self.filters.from_date, self.filters.to_date]),
	# 		},
	# 	)
	# 	self.entity_names = {}
	# 	for d in self.entries:
	# 		self.entity_names.setdefault(d.entity, d.entity_name)

	# def get_sales_transactions_based_on_items(self):

	# 	if self.filters["value_quantity"] == "Value":
	# 		value_field = "base_amount"
	# 	else:
	# 		value_field = "stock_qty"

	# 	self.entries = frappe.db.sql(
	# 		"""
	# 		select i.item_code as entity,i.warehouse, i.item_name as entity_name, i.stock_uom, i.{value_field} as value_field, s.{date_field}
	# 		from `tab{doctype} Item` i , `tab{doctype}` s	
	# 		where s.name = i.parent and i.docstatus = 1 and s.company = %s
	# 		and s.{date_field} between %s and %s
	# 	""".format(
	# 			date_field=self.date_field, value_field=value_field, doctype=self.filters.doc_type
	# 		),
	# 		(self.filters.company, self.filters.from_date, self.filters.to_date),
	# 		as_dict=1,
	# 	)
	# 	print('\n\n\n get_sales_transactions_based_on_items:-->',self.entries)
	# 	self.entity_names = {}
	# 	for d in self.entries:
	# 		self.entity_names.setdefault(d.entity, d.entity_name)
	# 	print('\n\n\n self.entity_names:-->',self.entity_names)
		
	# def get_sales_transactions_based_on_warehouse(self):

	# 	if self.filters["value_quantity"] == "Value":
	# 		value_field = "base_amount"
	# 	else:
	# 		value_field = "stock_qty"

	# 	self.entries = frappe.db.sql(
	# 		"""
	# 		select i.item_code as entity,i.warehouse, i.item_name as entity_name, i.stock_uom, i.{value_field} as value_field, s.{date_field}
	# 		from `tab{doctype} Item` i , `tab{doctype}` s	
	# 		where s.name = i.parent and i.docstatus = 1 and s.company = %s
	# 		and s.{date_field} between %s and %s
	# 	""".format(
	# 			date_field=self.date_field, value_field=value_field, doctype=self.filters.doc_type
	# 		),
	# 		(self.filters.company, self.filters.from_date, self.filters.to_date),
	# 		as_dict=1,
	# 	)
	# 	print('\n\n\n get_sales_transactions_based_on_items:-->',self.entries)
	# 	self.entity_names = {}
	# 	for d in self.entries:
	# 		self.entity_names.setdefault(d.entity, d.entity_name)
	# 	print('\n\n\n self.entity_names:-->',self.entity_names)

	# def get_sales_transactions_based_on_customer_or_territory_group(self):
	# 	if self.filters["value_quantity"] == "Value":
	# 		value_field = "base_net_total as value_field"
	# 	else:
	# 		value_field = "total_qty as value_field"

	# 	if self.filters.tree_type == "Customer Group":
	# 		entity_field = "customer_group as entity"
	# 	elif self.filters.tree_type == "Supplier Group":
	# 		entity_field = "supplier as entity"
	# 		self.get_supplier_parent_child_map()
	# 	else:
	# 		entity_field = "territory as entity"

	# 	self.entries = frappe.get_all(
	# 		self.filters.doc_type,
	# 		fields=[entity_field, value_field, self.date_field],
	# 		filters={
	# 			"docstatus": 1,
	# 			"company": self.filters.company,
	# 			self.date_field: ("between", [self.filters.from_date, self.filters.to_date]),
	# 		},
	# 	)
	# 	self.get_groups()

	# def get_sales_transactions_based_on_item_group(self):
	# 	if self.filters["value_quantity"] == "Value":
	# 		value_field = "base_amount"
	# 	else:
	# 		value_field = "qty"

	# 	self.entries = frappe.db.sql(
	# 		"""
	# 		select i.item_group as entity, i.{value_field} as value_field, s.{date_field}
	# 		from `tab{doctype} Item` i , `tab{doctype}` s
	# 		where s.name = i.parent and i.docstatus = 1 and s.company = %s
	# 		and s.{date_field} between %s and %s
	# 	""".format(
	# 			date_field=self.date_field, value_field=value_field, doctype=self.filters.doc_type
	# 		),
	# 		(self.filters.company, self.filters.from_date, self.filters.to_date),
	# 		as_dict=1,
	# 	)

	# 	self.get_groups()

	# def get_sales_transactions_based_on_project(self):
	# 	if self.filters["value_quantity"] == "Value":
	# 		value_field = "base_net_total as value_field"
	# 	else:
	# 		value_field = "total_qty as value_field"

	# 	entity = "project as entity"

	# 	self.entries = frappe.get_all(
	# 		self.filters.doc_type,
	# 		fields=[entity, value_field, self.date_field],
	# 		filters={
	# 			"docstatus": 1,
	# 			"company": self.filters.company,
	# 			"project": ["!=", ""],
	# 			self.date_field: ("between", [self.filters.from_date, self.filters.to_date]),
	# 		},
	# 	)

	# def get_rows_by_group(self):
	# 	self.get_periodic_data()
	# 	out = []

	# 	for d in reversed(self.group_entries):
	# 		row = {"entity": d.name, "indent": self.depth_map.get(d.name)}
	# 		total = 0
	# 		for end_date in self.periodic_daterange:
	# 			period = self.get_period(end_date)
	# 			amount = flt(self.entity_periodic_data.get(d.name, {}).get(period, 0.0))
	# 			row[scrub(period)] = amount
	# 			if d.parent and (self.filters.tree_type != "Order Type" or d.parent == "Order Types"):
	# 				self.entity_periodic_data.setdefault(d.parent, frappe._dict()).setdefault(period, 0.0)
	# 				self.entity_periodic_data[d.parent][period] += amount
	# 			total += amount

	# 		row["total"] = total
	# 		out = [row] + out

	# 	self.data = out
