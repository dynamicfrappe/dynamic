# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import frappe
from frappe import _, qb, scrub
from frappe.query_builder import Order
from frappe.utils import cint, flt

from erpnext.controllers.queries import get_match_cond
from erpnext.stock.report.stock_ledger.stock_ledger import get_item_group_condition
from erpnext.stock.utils import get_incoming_rate
import frappe
import os, json
from frappe import _
from frappe.modules import scrub, get_module_path
from frappe.utils import flt, cint, get_html_format
from frappe.translate import send_translations
import frappe.desk.reportview
from frappe.permissions import get_role_permissions
from six import iteritems, string_types

def execute(filters=None):
	if not filters:
		filters = frappe._dict()
	filters.currency = frappe.get_cached_value("Company", filters.company, "default_currency")

	gross_profit_data = GrossProfitGenerator(filters)

	data = []

	group_wise_columns = frappe._dict(
		{
			"invoice": [
				"invoice_or_item",
				"customer",
				"customer_group",
				"posting_date",
				"item_code",
				"item_name",
				"item_group",
				"brand",
				"cost_center",
				"description",
				"warehouse",
				"qty",
				"base_rate",
				"buying_rate",
				"base_amount",
				"buying_amount",
				"gross_profit",
				"gross_profit_percent",
				# "gross_profit_percent_demo",
				"project",
			],
			"item_code": [
				"item_code",
				"item_name",
				"brand",
				# "cost_center",
				"description",
				"qty",
				"base_rate",
				"buying_rate",
				"base_amount",
				"buying_amount",
				"gross_profit",
				"gross_profit_percent",
				# "gross_profit_percent_demo",
			],
			"warehouse": [
				"warehouse",
				"qty",
				"base_rate",
				"buying_rate",
				"base_amount",
				"buying_amount",
				"gross_profit",
				"gross_profit_percent",
				# "gross_profit_percent_demo",
			],
			"brand": [
				"brand",
				"qty",
				"base_rate",
				"buying_rate",
				"base_amount",
				"buying_amount",
				"gross_profit",
				"gross_profit_percent",
				# "gross_profit_percent_demo",
			],
			"item_group": [
				"item_group",
				"qty",
				"base_rate",
				"buying_rate",
				"base_amount",
				"buying_amount",
				"gross_profit",
				"gross_profit_percent",
				# "gross_profit_percent_demo",
			],
			"customer": [
				"customer",
				"customer_group",
				"qty",
				"base_rate",
				"buying_rate",
				"base_amount",
				"buying_amount",
				"gross_profit",
				"gross_profit_percent",
				# "gross_profit_percent_demo",
			],
			"customer_group": [
				"customer_group",
				"qty",
				"base_rate",
				"buying_rate",
				"base_amount",
				"buying_amount",
				"gross_profit",
				"gross_profit_percent",
				# "gross_profit_percent_demo",
			],
			"sales_person": [
				"sales_person",
				"allocated_amount",
				"qty",
				"base_rate",
				"buying_rate",
				"base_amount",
				"buying_amount",
				"gross_profit",
				"gross_profit_percent",
				# "gross_profit_percent_demo",
			],
			"project": ["project", "base_amount", "buying_amount", "gross_profit", "gross_profit_percent","gross_profit_percent_demo"],
			"territory": [
				"territory",
				"base_amount",
				"buying_amount",
				"gross_profit",
				"gross_profit_percent",
				# "gross_profit_percent_demo",
			],
		}
	)

	columns = get_columns(group_wise_columns, filters)

	if filters.group_by == "Invoice":
		get_data_when_grouped_by_invoice(columns, gross_profit_data, filters, group_wise_columns, data)

	else:
		get_data_when_not_grouped_by_invoice(gross_profit_data, filters, group_wise_columns, data)
	# data = add_total_row(data, columns)
	# frappe.errprint(f'data--->{data}')
	return columns, data


def get_data_when_grouped_by_invoice(
	columns, gross_profit_data, filters, group_wise_columns, data
):
	column_names = get_column_names()

	# to display item as Item Code: Item Name
	columns[0] = "Sales Invoice:Link/Item:300"
	# removing Item Code and Item Name columns
	del columns[4:6]

	for src in gross_profit_data.si_list:
		row = frappe._dict()
		row.indent = src.indent
		row.parent_invoice = src.parent_invoice
		row.currency = filters.currency

		for col in group_wise_columns.get(scrub(filters.group_by)):
			# frappe.errprint(f'-column_names[col]:{column_names[col]}-->{src.get(col)}')
			row[column_names[col]] = src.get(col)

		data.append(row)


def get_data_when_not_grouped_by_invoice(gross_profit_data, filters, group_wise_columns, data):
	# frappe.errprint(f"test--***->{gross_profit_data.grouped_data}")
	for src in gross_profit_data.grouped_data:
		# frappe.errprint(f"src--***->{src}")
		row = []
		for col in group_wise_columns.get(scrub(filters.group_by)):
			# frappe.errprint(f"col--***->{col}")
			# frappe.errprint(f"src.get(col)--***->{src.get(col)}")
			row.append(src.get(col,col))

		row.append(filters.currency)

		data.append(row)


def get_columns(group_wise_columns, filters):
	columns = []
	column_map = frappe._dict(
		{
			"parent": {
				"label": _("Sales Invoice"),
				"fieldname": "parent_invoice",
				"fieldtype": "Link",
				"options": "Sales Invoice",
				"width": 120,
			},
			"invoice_or_item": {
				"label": _("Sales Invoice"),
				"fieldtype": "Link",
				"options": "Sales Invoice",
				"width": 120,
			},
			"posting_date": {
				"label": _("Posting Date"),
				"fieldname": "posting_date",
				"fieldtype": "Date",
				"width": 100,
			},
			"posting_time": {
				"label": _("Posting Time"),
				"fieldname": "posting_time",
				"fieldtype": "Data",
				"width": 100,
			},
			"item_code": {
				"label": _("Item Code"),
				"fieldname": "item_code",
				"fieldtype": "Link",
				"options": "Item",
				"width": 100,
			},
			"item_name": {
				"label": _("Item Name"),
				"fieldname": "item_name",
				"fieldtype": "Data",
				"width": 100,
			},
			"item_group": {
				"label": _("Item Group"),
				"fieldname": "item_group",
				"fieldtype": "Link",
				"options": "Item Group",
				"width": 100,
			},
			"brand": {"label": _("Brand"), "fieldtype": "Link", "options": "Brand", "width": 100},
			"description": {
				"label": _("Description"),
				"fieldname": "description",
				"fieldtype": "Data",
				"width": 100,
			},
			"warehouse": {
				"label": _("Warehouse"),
				"fieldname": "warehouse",
				"fieldtype": "Link",
				"options": "warehouse",
				"width": 100,
			},
			"qty": {"label": _("Qty"), "fieldname": "qty", "fieldtype": "Float", "width": 80},
			"base_rate": {
				"label": _("Avg. Selling Rate"),
				"fieldname": "avg._selling_rate",
				"fieldtype": "Currency",
				"options": "currency",
				"width": 100,
			},
			"buying_rate": {
				"label": _("Valuation Rate"),
				"fieldname": "valuation_rate",
				"fieldtype": "Currency",
				"options": "currency",
				"width": 100,
			},
			"base_amount": {
				"label": _("Selling Amount"),
				"fieldname": "selling_amount",
				"fieldtype": "Currency",
				"options": "currency",
				"width": 100,
			},
			"buying_amount": {
				"label": _("Buying Amount"),
				"fieldname": "buying_amount",
				"fieldtype": "Currency",
				"options": "currency",
				"width": 100,
			},
			"gross_profit": {
				"label": _("Gross Profit"),
				"fieldname": "gross_profit",
				"fieldtype": "Currency",
				"options": "currency",
				"width": 100,
			},
			"gross_profit_percent": {
				"label": _("Gross Profit Percent"),
				"fieldname": "gross_profit_%",
				"fieldtype": "Percent",
				"width": 100,
			},
			# "gross_profit_percent_demo": {
			# 	"label": _("Gross Profit Percent Demo"),
			# 	"fieldname": "gross_profit_percent_demo",
			# 	"fieldtype": "Float",
			# 	"width": 100,
			# },
			"project": {
				"label": _("Project"),
				"fieldname": "project",
				"fieldtype": "Link",
				"options": "Project",
				"width": 100,
			},
			"sales_person": {
				"label": _("Sales Person"),
				"fieldname": "sales_person",
				"fieldtype": "Data",
				"width": 100,
			},
			"allocated_amount": {
				"label": _("Allocated Amount"),
				"fieldname": "allocated_amount",
				"fieldtype": "Currency",
				"options": "currency",
				"width": 100,
			},
			"customer": {
				"label": _("Customer"),
				"fieldname": "customer",
				"fieldtype": "Link",
				"options": "Customer",
				"width": 100,
			},
			"customer_group": {
				"label": _("Customer Group"),
				"fieldname": "customer_group",
				"fieldtype": "Link",
				"options": "customer",
				"width": 100,
			},
			"territory": {
				"label": _("Territory"),
				"fieldname": "territory",
				"fieldtype": "Link",
				"options": "territory",
				"width": 100,
			},
			
			"cost_center": {
				"label": _("Cost Center"),
				"fieldname": "cost_center",
				"fieldtype": "Link",
				"options": "Cost Center",
				"width": 100,
			},
			
		}
	)
	# frappe.errprint(group_wise_columns.get(scrub(filters.group_by)))
	for col in group_wise_columns.get(scrub(filters.group_by)):
		# frappe.errprint(f"col:-->{col}----")
		columns.append(column_map.get(col))

	columns.append(
		{
			"fieldname": "currency",
			"label": _("Currency"),
			"fieldtype": "Link",
			"options": "Currency",
			"hidden": 1,
		}
	)
	# columns.append(
	# 	{
	# 		"label": _("Cost Center"),
	# 		"fieldname": "cost_center",
	# 		"fieldtype": "Link",
	# 		"options": "Cost Center",
	# 		"width": 100,
	# 	}
	# )

	return columns


def get_column_names():
	return frappe._dict(
		{
			"invoice_or_item": "sales_invoice",
			"customer": "customer",
			"customer_group": "customer_group",
			"posting_date": "posting_date",
			"item_code": "item_code",
			"item_name": "item_name",
			"item_group": "item_group",
			"brand": "brand",
			"cost_center":"cost_center",
			"description": "description",
			"warehouse": "warehouse",
			"qty": "qty",
			"base_rate": "avg._selling_rate",
			"buying_rate": "valuation_rate",
			"base_amount": "selling_amount",
			"buying_amount": "buying_amount",
			"gross_profit": "gross_profit",
			"gross_profit_percent": "gross_profit_%",
			"project": "project",
			# "gross_profit_percent_demo":"gross_profit_percent_demo",
		}
	)


class  GrossProfitGenerator(object):
	def __init__(self, filters=None):
		self.sle = {}
		self.data = []
		self.average_buying_rate = {}
		self.filters = frappe._dict(filters)
		self.load_invoice_items()
		self.get_delivery_notes()

		if filters.group_by == "Invoice":
			self.group_items_by_invoice()

		self.load_product_bundle()
		self.load_non_stock_items()
		self.get_returned_invoice_items()
		self.process()

	def process(self):
		self.grouped = {}
		self.grouped_data = []

		self.currency_precision = cint(frappe.db.get_default("currency_precision")) or 3
		self.float_precision = cint(frappe.db.get_default("float_precision")) or 2

		grouped_by_invoice = True if self.filters.get("group_by") == "Invoice" else False

		if grouped_by_invoice:
			buying_amount = 0
			qty=0
		# print("\n\n\n\n---self.si_list---?",self.si_list,'\n\n\n')
		for row in reversed(self.si_list):
			if self.skip_row(row):
				continue

			row.base_amount = flt(row.base_net_amount, self.currency_precision)

			product_bundles = []
			if row.update_stock:
				product_bundles = self.product_bundles.get(row.parenttype, {}).get(row.parent, frappe._dict())
			elif row.dn_detail:
				product_bundles = self.product_bundles.get("Delivery Note", {}).get(
					row.delivery_note, frappe._dict()
				)
				row.item_row = row.dn_detail

			# get buying amount
			if row.item_code in product_bundles:
				row.buying_amount = flt(
					self.get_buying_amount_from_product_bundle(row, product_bundles[row.item_code]),
					self.currency_precision,
				)
			else:
				row.buying_amount = flt(self.get_buying_amount(row, row.item_code), self.currency_precision)
			#! sort from end (child of invoice)
			if grouped_by_invoice:
				if row.indent == 1.0:
					buying_amount += row.buying_amount
					qty +=  row.qty
				elif row.indent == 0.0:
					row.buying_amount = buying_amount
					buying_amount = 0
					row.qty = qty
					qty = 0

			# get buying rate
			if flt(row.qty):
				row.buying_rate = flt(row.buying_amount / flt(row.qty), self.float_precision)
				row.base_rate = flt(row.base_amount / flt(row.qty), self.float_precision)
				# if(row.item_code=='10359004'):
				# 	print("\n\n\n\n------?",row.item_name,row.base_amount,'\n\n\n')
			else:
				if self.is_not_invoice_row(row):
					row.buying_rate, row.base_rate = 0.0, 0.0

			# calculate gross profit
			row.gross_profit = flt(row.base_amount - row.buying_amount, self.currency_precision)
			if row.base_amount:
				row.gross_profit_percent = flt(
					(row.gross_profit / row.base_amount) * 100.0, self.currency_precision
				)
				# row.gross_profit_percent = 60.33
			else:
				row.gross_profit_percent = 0.0

			# add to grouped
			self.grouped.setdefault(row.get(scrub(self.filters.group_by)), []).append(row)

		if self.grouped:
			self.get_average_rate_based_on_group_by()
		# frappe.errprint(f"self.grouped_data --->{self.grouped_data}")

	def get_average_rate_based_on_group_by(self):
		for key in list(self.grouped):
			if self.filters.get("group_by") != "Invoice":
				for i, row in enumerate(self.grouped[key]):
					if i == 0:
						new_row = row
					else:
						new_row.qty += flt(row.qty)
						new_row.buying_amount += flt(row.buying_amount, self.currency_precision)
						new_row.base_amount += flt(row.base_amount, self.currency_precision)
				new_row = self.set_average_rate(new_row)
				self.grouped_data.append(new_row)
			else:
				for i, row in enumerate(self.grouped[key]):
					if row.indent == 1.0:
						if (
							row.parent in self.returned_invoices and row.item_code in self.returned_invoices[row.parent]
						):
							returned_item_rows = self.returned_invoices[row.parent][row.item_code]
							for returned_item_row in returned_item_rows:
								# returned_items 'qty' should be stateful
								if returned_item_row.qty != 0:
									if row.qty >= abs(returned_item_row.qty):
										row.qty += returned_item_row.qty
										returned_item_row.qty = 0
									else:
										row.qty = 0
										returned_item_row.qty += row.qty
								row.base_amount += flt(returned_item_row.base_amount, self.currency_precision)
							row.buying_amount = flt(flt(row.qty) * flt(row.buying_rate), self.currency_precision)
						if flt(row.qty) or row.base_amount:
							row = self.set_average_rate(row)
							self.grouped_data.append(row)

	def is_not_invoice_row(self, row):
		return (self.filters.get("group_by") == "Invoice" and row.indent != 0.0) or self.filters.get(
			"group_by"
		) != "Invoice"

	def set_average_rate(self, new_row):
		self.set_average_gross_profit(new_row)
		new_row.buying_rate = (
			flt(new_row.buying_amount / new_row.qty, self.float_precision) if new_row.qty else 0
		)
		new_row.base_rate = (
			flt(new_row.base_amount / new_row.qty, self.float_precision) if new_row.qty else 0
		)
		return new_row

	def set_average_gross_profit(self, new_row):
		
		new_row.gross_profit = flt(new_row.base_amount - new_row.buying_amount, self.currency_precision)
		new_row.gross_profit_percent = (
			flt(((new_row.gross_profit / new_row.base_amount) * 100.0), self.currency_precision)
			if new_row.base_amount
			else 0
		)
		# new_row.gross_profit_percent_demo = (
		# 	flt(((new_row.gross_profit / new_row.base_amount)), self.currency_precision)
		# 	if new_row.base_amount
		# 	else 0
		# )
		new_row.buying_rate = (
			flt(new_row.buying_amount / flt(new_row.qty), self.float_precision) if flt(new_row.qty) else 0
		)
		new_row.base_rate = (
			flt(new_row.base_amount / flt(new_row.qty), self.float_precision) if flt(new_row.qty) else 0
		)

	def get_returned_invoice_items(self):
		returned_invoices = frappe.db.sql(
			"""
			select
				si.name, si_item.item_code, si_item.stock_qty as qty, si_item.base_net_amount as base_amount, si.return_against
			from
				`tabSales Invoice` si, `tabSales Invoice Item` si_item
			where
				si.name = si_item.parent
				and si.docstatus = 1
				and si.is_return = 1
		""",
			as_dict=1,
		)

		self.returned_invoices = frappe._dict()
		for inv in returned_invoices:
			self.returned_invoices.setdefault(inv.return_against, frappe._dict()).setdefault(
				inv.item_code, []
			).append(inv)

	def skip_row(self, row):
		if self.filters.get("group_by") != "Invoice":
			if not row.get(scrub(self.filters.get("group_by", ""))):
				return True

		return False

	def get_buying_amount_from_product_bundle(self, row, product_bundle):
		# frappe.errprint("in get_buying_amount_from_product_bundle")
		buying_amount = 0.0
		for packed_item in product_bundle:
			if packed_item.get("parent_detail_docname") == row.item_row:
				buying_amount += self.get_buying_amount(row, packed_item.item_code)

		return flt(buying_amount, self.currency_precision)

	def calculate_buying_amount_from_sle(self, row, my_sle, parenttype, parent, item_row, item_code):
		for i, sle in enumerate(my_sle):
			# find the stock valution rate from stock ledger entry
			if (
				sle.voucher_type == parenttype
				and parent == sle.voucher_no
				and sle.voucher_detail_no == item_row
			):
				previous_stock_value = len(my_sle) > i + 1 and flt(my_sle[i + 1].stock_value) or 0.0

				if previous_stock_value:
					return abs(previous_stock_value - flt(sle.stock_value)) * flt(row.qty) / abs(flt(sle.qty))
				else:
					return flt(row.qty) * self.get_average_buying_rate(row, item_code)
		return 0.0

	def get_buying_amount(self, row, item_code):
		# frappe.errprint(f'--in get_buying_amount 566-->{row}')
		# IMP NOTE
		# stock_ledger_entries should already be filtered by item_code and warehouse and
		# sorted by posting_date desc, posting_time desc
		if item_code in self.non_stock_items and (row.project or row.cost_center):
			# Issue 6089-Get last purchasing rate for non-stock item
			item_rate = self.get_last_purchase_rate(item_code, row)
			return flt(row.qty) * item_rate

		else:
			my_sle = self.get_stock_ledger_entries(item_code, row.warehouse)
			if (row.update_stock or row.dn_detail) and my_sle:
				parenttype, parent = row.parenttype, row.parent
				if row.dn_detail:
					parenttype, parent = "Delivery Note", row.delivery_note

				return self.calculate_buying_amount_from_sle(
					row, my_sle, parenttype, parent, row.item_row, item_code
				)
			elif self.delivery_notes.get((row.parent, row.item_code), None):
				#  check if Invoice has delivery notes
				dn = self.delivery_notes.get((row.parent, row.item_code))
				parenttype, parent, item_row, warehouse = (
					"Delivery Note",
					dn["delivery_note"],
					dn["item_row"],
					dn["warehouse"],
				)
				my_sle = self.get_stock_ledger_entries(item_code, row.warehouse)
				return self.calculate_buying_amount_from_sle(
					row, my_sle, parenttype, parent, item_row, item_code
				)
			elif row.sales_order and row.so_detail:
				incoming_amount = self.get_buying_amount_from_so_dn(row.sales_order, row.so_detail, item_code)
				if incoming_amount:
					return incoming_amount
			else:
				return flt(row.qty) * self.get_average_buying_rate(row, item_code)

		return flt(row.qty) * self.get_average_buying_rate(row, item_code)

	def get_buying_amount_from_so_dn(self, sales_order, so_detail, item_code):
		from frappe.query_builder.functions import Sum

		delivery_note_item = frappe.qb.DocType("Delivery Note Item")

		query = (
			frappe.qb.from_(delivery_note_item)
			.select(Sum(delivery_note_item.incoming_rate * delivery_note_item.stock_qty))
			.where(delivery_note_item.docstatus == 1)
			.where(delivery_note_item.item_code == item_code)
			.where(delivery_note_item.against_sales_order == sales_order)
			.where(delivery_note_item.so_detail == so_detail)
			.groupby(delivery_note_item.item_code)
		)

		incoming_amount = query.run()
		return flt(incoming_amount[0][0]) if incoming_amount else 0

	def get_average_buying_rate(self, row, item_code):
		args = row
		if not item_code in self.average_buying_rate:
			args.update(
				{
					"voucher_type": row.parenttype,
					"voucher_no": row.parent,
					"allow_zero_valuation": True,
					"company": self.filters.company,
				}
			)

			average_buying_rate = get_incoming_rate(args)
			self.average_buying_rate[item_code] = flt(average_buying_rate)

		return self.average_buying_rate[item_code]

	def get_last_purchase_rate(self, item_code, row):
		# frappe.errprint(f'--get_last_purchase_rate-->{row}')
		purchase_invoice = frappe.qb.DocType("Purchase Invoice")
		purchase_invoice_item = frappe.qb.DocType("Purchase Invoice Item")

		query = (
			frappe.qb.from_(purchase_invoice_item)
			.inner_join(purchase_invoice)
			.on(purchase_invoice.name == purchase_invoice_item.parent)
			.select(purchase_invoice_item.base_rate / purchase_invoice_item.conversion_factor)
			.where(purchase_invoice.docstatus == 1)
			.where(purchase_invoice.posting_date <= self.filters.to_date)
			.where(purchase_invoice_item.item_code == item_code)
		)

		if row.project:
			query.where(purchase_invoice_item.project == row.project)

		if row.cost_center:
			query.where(purchase_invoice_item.cost_center == row.cost_center)

		query.orderby(purchase_invoice.posting_date, order=frappe.qb.desc)
		query.limit(1)
		last_purchase_rate = query.run()

		return flt(last_purchase_rate[0][0]) if last_purchase_rate else 0

	def load_invoice_items(self):
		conditions = ""
		if self.filters.company:
			conditions += " and company = %(company)s"
		if self.filters.from_date:
			conditions += " and posting_date >= %(from_date)s"
		if self.filters.to_date:
			conditions += " and posting_date <= %(to_date)s"

		conditions += " and (is_return = 0 or (is_return=1 and return_against is null))"

		if self.filters.item_group:
			conditions += " and {0}".format(get_item_group_condition(self.filters.item_group))

		if self.filters.sales_person:
			conditions += """
				and exists(select 1
							from `tabSales Team` st
							where st.parent = `tabSales Invoice`.name
							and   st.sales_person = %(sales_person)s)
			"""

		if self.filters.group_by == "Sales Person":
			sales_person_cols = ", sales.sales_person, sales.allocated_amount, sales.incentives"
			sales_team_table = "left join `tabSales Team` sales on sales.parent = `tabSales Invoice`.name"
		else:
			sales_person_cols = ""
			sales_team_table = ""

		if self.filters.get("sales_invoice"):
			conditions += " and `tabSales Invoice`.name = %(sales_invoice)s"

		if self.filters.get("item_code"):
			conditions += " and `tabSales Invoice Item`.item_code = %(item_code)s"
			
		if self.filters.get("customer"):
			conditions += f" and `tabSales Invoice`.customer = '{self.filters.get('customer')}' "

		self.si_list = frappe.db.sql(
			"""
			select
				`tabSales Invoice Item`.parenttype, `tabSales Invoice Item`.parent,
				`tabSales Invoice`.posting_date, `tabSales Invoice`.posting_time,
				`tabSales Invoice`.project, `tabSales Invoice`.update_stock,
				`tabSales Invoice`.customer, `tabSales Invoice`.customer_group,
				`tabSales Invoice`.territory, `tabSales Invoice Item`.item_code,
				`tabSales Invoice Item`.item_name, `tabSales Invoice Item`.description,
				`tabSales Invoice Item`.warehouse, `tabSales Invoice Item`.item_group,
				`tabSales Invoice Item`.brand, `tabSales Invoice Item`.so_detail,
				`tabSales Invoice Item`.sales_order, `tabSales Invoice Item`.dn_detail,
				`tabSales Invoice Item`.delivery_note, `tabSales Invoice Item`.stock_qty as qty,
				`tabSales Invoice Item`.base_net_rate, `tabSales Invoice Item`.base_net_amount,
				`tabSales Invoice Item`.name as "item_row", `tabSales Invoice`.is_return,
				`tabSales Invoice Item`.cost_center
				{sales_person_cols}
			from
				`tabSales Invoice` inner join `tabSales Invoice Item`
					on `tabSales Invoice Item`.parent = `tabSales Invoice`.name
				{sales_team_table}
			where
				`tabSales Invoice`.docstatus=1 and `tabSales Invoice`.is_opening!='Yes' {conditions} {match_cond}
			order by
				`tabSales Invoice`.posting_date desc, `tabSales Invoice`.posting_time desc""".format(
				conditions=conditions,
				sales_person_cols=sales_person_cols,
				sales_team_table=sales_team_table,
				match_cond=get_match_cond("Sales Invoice"),
			),
			self.filters,
			as_dict=1,
		)
		# frappe.errprint(self.si_list)

	def get_delivery_notes(self):
		self.delivery_notes = frappe._dict({})
		if self.si_list:
			invoices = [x.parent for x in self.si_list]
			dni = qb.DocType("Delivery Note Item")
			delivery_notes = (
				qb.from_(dni)
				.select(
					dni.against_sales_invoice.as_("sales_invoice"),
					dni.item_code,
					dni.warehouse,
					dni.parent.as_("delivery_note"),
					dni.name.as_("item_row"),
				)
				.where((dni.docstatus == 1) & (dni.against_sales_invoice.isin(invoices)))
				.groupby(dni.against_sales_invoice, dni.item_code)
				.orderby(dni.creation, order=Order.desc)
				.run(as_dict=True)
			)

			for entry in delivery_notes:
				self.delivery_notes[(entry.sales_invoice, entry.item_code)] = entry

	def group_items_by_invoice(self):
		"""
		Turns list of Sales Invoice Items to a tree of Sales Invoices with their Items as children.
		"""

		parents = []

		for row in self.si_list:
			# frappe.errprint(f'parent-->{row}')
			if row.parent not in parents:
				parents.append(row.parent)

		parents_index = 0
		# frappe.errprint(f'before si_list++++++-->{self.si_list}')
		for index, row in enumerate(self.si_list):
			if parents_index < len(parents) and row.parent == parents[parents_index]:
				invoice = self.get_invoice_row(row)
				# frappe.errprint(f'invoice row++++++-->{invoice}')
				self.si_list.insert(index, invoice)
				parents_index += 1

			else:
				# skipping the bundle items rows
				if not row.indent:
					row.indent = 1.0
					row.parent_invoice = row.parent
					row.invoice_or_item = row.item_code

					if frappe.db.exists("Product Bundle", row.item_code):
						self.add_bundle_items(row, index)
		# frappe.errprint(f'self.si_list++++++-->{self.si_list}')

	def get_invoice_row(self, row):
		return frappe._dict(
			{
				"parent_invoice": "",
				"indent": 0.0,
				"invoice_or_item": row.parent,
				"parent": None,
				"posting_date": row.posting_date,
				"posting_time": row.posting_time,
				"project": row.project,
				"update_stock": row.update_stock,
				"customer": row.customer,
				"customer_group": row.customer_group,
				"item_code": None,
				"item_name": None,
				"description": '',
				"warehouse": None,
				"item_group": None,
				"brand": None,
				"dn_detail": None,
				"delivery_note": None,
				"qty": 0,
				"item_row": None,
				"is_return": row.is_return,
				"cost_center": row.cost_center,
				"base_net_amount": frappe.db.get_value("Sales Invoice", row.parent, "base_net_total"),
			}
		)

	def add_bundle_items(self, product_bundle, index):
		bundle_items = self.get_bundle_items(product_bundle)

		for i, item in enumerate(bundle_items):
			bundle_item = self.get_bundle_item_row(product_bundle, item)
			self.si_list.insert((index + i + 1), bundle_item)

	def get_bundle_items(self, product_bundle):
		return frappe.get_all(
			"Product Bundle Item", filters={"parent": product_bundle.item_code}, fields=["item_code", "qty"]
		)

	def get_bundle_item_row(self, product_bundle, item):
		item_name, description, item_group, brand = self.get_bundle_item_details(item.item_code)

		return frappe._dict(
			{
				"parent_invoice": product_bundle.item_code,
				"indent": product_bundle.indent + 1,
				"parent": None,
				"invoice_or_item": item.item_code,
				"posting_date": product_bundle.posting_date,
				"posting_time": product_bundle.posting_time,
				"project": product_bundle.project,
				"customer": product_bundle.customer,
				"customer_group": product_bundle.customer_group,
				"item_code": item.item_code,
				"item_name": item_name,
				"description": description,
				"warehouse": product_bundle.warehouse,
				"item_group": item_group,
				"brand": brand,
				"dn_detail": product_bundle.dn_detail,
				"delivery_note": product_bundle.delivery_note,
				"qty": (flt(product_bundle.qty) * flt(item.qty)),
				"item_row": None,
				"is_return": product_bundle.is_return,
				"cost_center": product_bundle.cost_center,
			}
		)

	def get_bundle_item_details(self, item_code):
		return frappe.db.get_value(
			"Item", item_code, ["item_name", "description", "item_group", "brand"]
		)

	def get_stock_ledger_entries(self, item_code, warehouse):
		# frappe.errprint(f'--in get_stock_ledger_entries 77-->')
		if item_code and warehouse:
			if (item_code, warehouse) not in self.sle:
				sle = qb.DocType("Stock Ledger Entry")
				res = (
					qb.from_(sle)
					.select(
						sle.item_code,
						sle.voucher_type,
						sle.voucher_no,
						sle.voucher_detail_no,
						sle.stock_value,
						sle.warehouse,
						sle.actual_qty.as_("qty"),
					)
					.where(
						(sle.company == self.filters.company)
						& (sle.item_code == item_code)
						& (sle.warehouse == warehouse)
						& (sle.is_cancelled == 0)
					)
					.orderby(sle.item_code)
					.orderby(sle.warehouse, sle.posting_date, sle.posting_time, sle.creation, order=Order.desc)
					.run(as_dict=True)
				)

				self.sle[(item_code, warehouse)] = res
			# frappe.errprint(f'--in res 88-->{res}')
			return self.sle[(item_code, warehouse)]
		return []

	def load_product_bundle(self):
		self.product_bundles = {}

		for d in frappe.db.sql(
			"""select parenttype, parent, parent_item,
			item_code, warehouse, -1*qty as total_qty, parent_detail_docname
			from `tabPacked Item` where docstatus=1""",
			as_dict=True,
		):
			self.product_bundles.setdefault(d.parenttype, frappe._dict()).setdefault(
				d.parent, frappe._dict()
			).setdefault(d.parent_item, []).append(d)

	def load_non_stock_items(self):
		self.non_stock_items = frappe.db.sql_list(
			"""select name from tabItem
			where is_stock_item=0"""
		)


# def add_total_row(result, columns):
# 	total_row = [""]*len(columns)
# 	has_percent = []
# 	for row in result:
# 		for i, col in enumerate(columns):
# 			fieldtype = None
# 			if isinstance(col, basestring):
# 				col = col.split(":")
# 				if len(col) > 1:
# 					fieldtype = col[1]
# 			else:
# 				fieldtype = col.get("fieldtype")

# 			if fieldtype in ["Currency", "Int", "Float", "Percent"] and flt(row[i]):
# 				total_row[i] = flt(total_row[i]) + flt(row[i])
# 			if fieldtype == "Percent" and i not in has_percent:
# 				has_percent.append(i)

# 	for i in has_percent:
# 		total_row[i] = total_row[i] / len(result)

# 	first_col_fieldtype = None
# 	if isinstance(columns[0], basestring):
# 		first_col = columns[0].split(":")
# 		if len(first_col) > 1:
# 			first_col_fieldtype = first_col[1].split("/")[0]
# 	else:
# 		first_col_fieldtype = columns[0].get("fieldtype")

# 	if first_col_fieldtype not in ["Currency", "Int", "Float", "Percent"]:
# 		if first_col_fieldtype == "Link":
# 			total_row[0] = "'" + _("Total") + "'"
# 		else:
# 			total_row[0] = _("Total")

# 	result.append(total_row)
# 	return result

# def add_total_row(result, columns, meta=None, is_tree=False, parent_field=None):
# 	print("\n\n\n\n-->tota*****l\n\n\n")
# 	total_row = [""] * len(columns)
# 	has_percent = []

# 	for i, col in enumerate(columns):
# 		fieldtype, options, fieldname = None, None, None
# 		if isinstance(col, string_types):
# 			if meta:
# 				# get fieldtype from the meta
# 				field = meta.get_field(col)
# 				if field:
# 					fieldtype = meta.get_field(col).fieldtype
# 					fieldname = meta.get_field(col).fieldname
# 			else:
# 				col = col.split(":")
# 				if len(col) > 1:
# 					if col[1]:
# 						fieldtype = col[1]
# 						if "/" in fieldtype:
# 							fieldtype, options = fieldtype.split("/")
# 					else:
# 						fieldtype = "Data"
# 		else:
# 			fieldtype = col.get("fieldtype")
# 			fieldname = col.get("fieldname")
# 			options = col.get("options")

# 		for row in result:
# 			if i >= len(row):
# 				continue
# 			cell = row.get(fieldname) if isinstance(row, dict) else row[i]
# 			if fieldtype in ["Currency", "Int", "Float", "Percent", "Duration"] and flt(cell):
# 				if not (is_tree and row.get(parent_field)):
# 					total_row[i] = flt(total_row[i]) + flt(cell)

# 			if fieldtype == "Percent" and i not in has_percent:
# 				has_percent.append(i)

# 			if fieldtype == "Time" and cell:
# 				if not total_row[i]:
# 					total_row[i] = timedelta(hours=0, minutes=0, seconds=0)
# 				total_row[i] = total_row[i] + cell

# 		if fieldtype == "Link" and options == "Currency":
# 			total_row[i] = result[0].get(fieldname) if isinstance(result[0], dict) else result[0][i]

# 	for i in has_percent:
# 		total_row[i] = flt(total_row[i]) / len(result)

# 	first_col_fieldtype = None
# 	if isinstance(columns[0], string_types):
# 		first_col = columns[0].split(":")
# 		if len(first_col) > 1:
# 			first_col_fieldtype = first_col[1].split("/")[0]
# 	else:
# 		first_col_fieldtype = columns[0].get("fieldtype")

# 	if first_col_fieldtype not in ["Currency", "Int", "Float", "Percent", "Date"]:
# 		total_row[0] = _("Total")

# 	result.append(total_row)
# 	return result
