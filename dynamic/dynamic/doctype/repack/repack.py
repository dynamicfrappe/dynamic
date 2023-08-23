# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from erpnext.stock.doctype.stock_entry.stock_entry import StockEntry
from six import iteritems, itervalues, string_types
from frappe.utils import cint, comma_or, cstr, flt, format_time, formatdate, getdate, nowdate
from erpnext.manufacturing.doctype.bom.bom import add_additional_cost, validate_bom_no
from frappe.model.mapper import get_mapped_doc
import json
from erpnext.stock.get_item_details import (
	get_bin_details,
	get_conversion_factor,
	get_default_cost_center,
	get_reserved_qty_for_so,
)

class Repack(StockEntry):

	def validate(self):
		# self.super()
		# super(Reback, self).validate()
		self.validate_warehouse()
	

	def on_submit(self):
		...


	def validate_warehouse(self):
		"""perform various (sometimes conditional) validations on warehouse"""
		
		# frappe.errprint('in first 1')
		source_mandatory = [
			"Material Issue",
			"Material Transfer",
			"Send to Subcontractor",
			"Material Transfer for Manufacture",
			"Material Consumption for Manufacture",
			"Repack",

		]

		target_mandatory = [
			"Material Receipt",
			"Material Transfer",
			"Send to Subcontractor",
			"Material Transfer for Manufacture",
			# "Repack",
		]

		validate_for_manufacture = any([d.bom_no for d in self.get("items")])

		# frappe.errprint(f'{self.purpose},{},{}')
		if self.purpose in source_mandatory and self.purpose not in target_mandatory:
			self.to_warehouse = None
			for d in self.get("items"):
				if(d.idx!=len(self.get("items"))):
					d.t_warehouse = None# self.to_warehouse
		# elif self.purpose in target_mandatory and self.purpose not in source_mandatory:
		# 	self.from_warehouse = None
		# 	for d in self.get("items"):
		# 		d.s_warehouse = None

		# for d in self.get("items"):
		# 	if not d.s_warehouse and not d.t_warehouse:
		# 		d.s_warehouse = self.from_warehouse
		# 		d.t_warehouse = self.to_warehouse

			# if self.purpose in source_mandatory and not d.s_warehouse:
			# 	if self.from_warehouse:
			# 		d.s_warehouse = self.from_warehouse
			# 	else:
			# 		frappe.throw(_("Source warehouse is mandatory for row {0}").format(d.idx))

			# if self.purpose in target_mandatory and not d.t_warehouse:
			# 	if self.to_warehouse:
			# 		d.t_warehouse = self.to_warehouse
			# 	else:
			# 		frappe.throw(_("Target warehouse is mandatory for row {0}").format(d.idx))

			# if self.purpose == "Manufacture":
			# 	if validate_for_manufacture:
			# 		if d.is_finished_item or d.is_scrap_item or d.is_process_loss:
			# 			d.s_warehouse = None
			# 			if not d.t_warehouse:
			# 				frappe.throw(_("Target warehouse is mandatory for row {0}").format(d.idx))
			# 		else:
			# 			d.t_warehouse = None
			# 			if not d.s_warehouse:
			# 				frappe.throw(_("Source warehouse is mandatory for row {0}").format(d.idx))

			# if (
			# 	cstr(d.s_warehouse) == cstr(d.t_warehouse)
			# 	and not self.purpose == "Material Transfer for Manufacture"
			# ):
			# 	frappe.throw(_("Source and target warehouse cannot be same for row {0}").format(d.idx))

			# if not (d.s_warehouse or d.t_warehouse):
			# 	frappe.throw(_("Atleast one warehouse is mandatory"))
	
	@frappe.whitelist()
	def get_items(self):
		self.set("items", [])
		self.validate_work_order()

		if not self.posting_date or not self.posting_time:
			frappe.throw(_("Posting date and posting time is mandatory"))

		self.set_work_order_details()
		self.flags.backflush_based_on = frappe.db.get_single_value(
			"Manufacturing Settings", "backflush_raw_materials_based_on"
		)

		if self.bom_no:

			backflush_based_on = frappe.db.get_single_value(
				"Manufacturing Settings", "backflush_raw_materials_based_on"
			)

			if self.purpose in [
				"Material Issue",
				"Material Transfer",
				"Manufacture",
				"Repack",
				"Send to Subcontractor",
				"Material Transfer for Manufacture",
				"Material Consumption for Manufacture",
			]:

				if self.work_order and self.purpose == "Material Transfer for Manufacture":
					item_dict = self.get_pending_raw_materials(backflush_based_on)
					if self.to_warehouse and self.pro_doc:
						for item in itervalues(item_dict):
							item["to_warehouse"] = self.pro_doc.wip_warehouse
					self.add_to_stock_entry_detail(item_dict)

				elif (
					self.work_order
					and (self.purpose == "Manufacture" or self.purpose == "Material Consumption for Manufacture")
					and not self.pro_doc.skip_transfer
					and self.flags.backflush_based_on == "Material Transferred for Manufacture"
				):
					self.get_transfered_raw_materials()

				elif (
					self.work_order
					and (self.purpose == "Manufacture" or self.purpose == "Material Consumption for Manufacture")
					and self.flags.backflush_based_on == "BOM"
					and frappe.db.get_single_value("Manufacturing Settings", "material_consumption") == 1
				):
					self.get_unconsumed_raw_materials()

				else:
					if not self.fg_completed_qty:
						frappe.throw(_("Manufacturing Quantity is mandatory"))

					item_dict = self.get_bom_raw_materials(self.fg_completed_qty)

					# Get PO Supplied Items Details
					if self.purchase_order and self.purpose == "Send to Subcontractor":
						# Get PO Supplied Items Details
						item_wh = frappe._dict(
							frappe.db.sql(
								"""
							SELECT
								rm_item_code, reserve_warehouse
							FROM
								`tabPurchase Order` po, `tabPurchase Order Item Supplied` poitemsup
							WHERE
								po.name = poitemsup.parent and po.name = %s """,
								self.purchase_order,
							)
						)

					for item in itervalues(item_dict):
						if self.pro_doc and cint(self.pro_doc.from_wip_warehouse):
							item["from_warehouse"] = self.pro_doc.wip_warehouse
						# Get Reserve Warehouse from PO
						if self.purchase_order and self.purpose == "Send to Subcontractor":
							item["from_warehouse"] = item_wh.get(item.item_code)
						item["to_warehouse"] = self.to_warehouse if self.purpose == "Send to Subcontractor" else ""

					self.add_to_stock_entry_detail(item_dict)

			# fetch the serial_no of the first stock entry for the second stock entry
			if self.work_order and self.purpose == "Manufacture":
				self.set_serial_nos(self.work_order)
				work_order = frappe.get_doc("Work Order", self.work_order)
				add_additional_cost(self, work_order)

			# add finished goods item
			if self.purpose in ("Manufacture", "Repack"):
				self.load_items_from_bom()

		self.set_scrap_items()
		self.set_actual_qty()
		self.update_items_for_process_loss()
		self.validate_customer_provided_item()
		self.calculate_rate_and_amount(raise_error_if_no_rate=False)
	
	def add_to_stock_entry_detail(self, item_dict, bom_no=None):
		for d in item_dict:
			item_row = item_dict[d]
			# frappe.errprint(item_row.get('rate'))
			# frappe.errprint(item_row)
			stock_uom = item_row.get("stock_uom") or frappe.db.get_value("Item", d, "stock_uom")

			se_child = self.append("items")
			se_child.s_warehouse = item_row.get("from_warehouse")
			se_child.t_warehouse = item_row.get("to_warehouse")
			se_child.item_code = item_row.get("item_code") or cstr(d)
			se_child.uom = item_row["uom"] if item_row.get("uom") else stock_uom
			se_child.stock_uom = stock_uom
			se_child.qty = flt(item_row["qty"], se_child.precision("qty"))
			# se_child.rate = item_row['rate']
			se_child.basic_rate = item_row.get('rate')
			se_child.allow_alternative_item = item_row.get("allow_alternative_item", 0)
			se_child.subcontracted_item = item_row.get("main_item_code")
			se_child.cost_center = item_row.get("cost_center") or get_default_cost_center(
				item_row, company=self.company
			)
			se_child.is_finished_item = item_row.get("is_finished_item", 0)
			se_child.is_scrap_item = item_row.get("is_scrap_item", 0)
			se_child.is_process_loss = item_row.get("is_process_loss", 0)

			for field in [
				"po_detail",
				"original_item",
				"expense_account",
				"description",
				"item_name",
				"serial_no",
				"batch_no",
				"allow_zero_valuation_rate",
			]:
				if item_row.get(field):
					se_child.set(field, item_row.get(field))

			if se_child.s_warehouse == None:
				se_child.s_warehouse = self.from_warehouse
			if se_child.t_warehouse == None:
				se_child.t_warehouse = self.to_warehouse

			# in stock uom
			se_child.conversion_factor = flt(item_row.get("conversion_factor")) or 1
			se_child.transfer_qty = flt(
				item_row["qty"] * se_child.conversion_factor, se_child.precision("qty")
			)

			se_child.bom_no = bom_no  # to be assigned for finished item
			se_child.job_card_item = item_row.get("job_card_item") if self.get("job_card") else None


@frappe.whitelist()
def get_row_qty(source_doc,item_code,edit_row_qty):
	reback = json.loads(source_doc)
	bom = reback.get('bom_no')
	data = frappe.db.sql(
		f"""
	SELECT stock_qty as qty FROM `tabBOM Explosion Item` WHERE item_code='{item_code}' and parent='{bom}'
	""",as_dict=1)
	if not len(data):
		msg = (_(f"QTY  should be 1"))
		return {'flage':False,'qty':1,'msg':msg}
	# print('\n\n\n-->data--',data,'\n\n\n')
	precent_change = frappe.db.get_single_value('Manufacturing Settings','change_precent') or 0
	if precent_change and data:
		data =data[0]
		if len(data) and data.get('qty'):
			if (
				float(edit_row_qty) < (data.get('qty') - (data.get('qty')*float(precent_change)/100) )
				or float(edit_row_qty) > (data.get('qty') + (data.get('qty')*float(precent_change)/100) ) 
			):
				msg = (_(f"QTY at least should be {(data.get('qty') - (data.get('qty')*float(precent_change)/100) )} AND No More {(data.get('qty') + (data.get('qty')*float(precent_change)/100) )}"))
				return {'flage':False,'qty':data.get('qty'),'msg':msg}

@frappe.whitelist()
def make_stock_entry(source_name, target_doc=None):
	doc = get_mapped_doc("Repack", source_name, {
		"Repack": {
			"doctype": "Stock Entry",
			"field_map": {
				'from_warehouse':'from_warehouse',
				'to_warehouse':'to_warehouse',
			},
			"field_no_map": {
				'bom_no':'bom_no',
			},
			"validation": {
				# "docstatus": ["=", 1]
			}
		},
		"Repack Items": {
			"doctype": "Stock Entry Detail",
			"field_map": {
				# "parent": "sales_order",
				# "uom": "stock_uom"
			},
			# "postprocess": update_item
		},
		
	}, target_doc)
	doc.repack = source_name
	return doc