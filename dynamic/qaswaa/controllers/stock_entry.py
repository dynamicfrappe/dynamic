import frappe
from frappe.contacts.doctype.address.address import get_company_address
from frappe.model.utils import get_fetch_values
from frappe.utils import add_days, cint, cstr, flt, get_link_to_form, getdate, nowdate, strip_html
from frappe.model.mapper import get_mapped_doc


from erpnext.stock.doctype.item.item import get_item_defaults
from erpnext.setup.doctype.item_group.item_group import get_item_group_defaults





@frappe.whitelist()
def make_stock_entry(source_name, target_doc=None, skip_item_mapping=False):
	def set_missing_values(source, target):
		target.run_method("set_missing_values")
		target.run_method("set_po_nos")
		# target.run_method("calculate_taxes_and_totals")

		if source.company:
			target.update({"company": source.company})
		else:
			# set company address
			target.update(get_company_address(target.company))

		if target.company:
			target.update(get_fetch_values("Stock Entry", "company", target.company))

		target.old_stock_entry = source.name	
        
	# def update_item(source, target, source_parent):
	# 	target.base_amount = (flt(source.qty) - flt(source.delivered_qty)) * flt(source.base_rate)
	# 	target.amount = (flt(source.qty) - flt(source.delivered_qty)) * flt(source.rate)
	# 	target.qty = flt(source.qty) - flt(source.delivered_qty)

	# 	item = get_item_defaults(target.item_code, source_parent.company)
	# 	item_group = get_item_group_defaults(target.item_code, source_parent.company)

	# 	if item:
	# 		target.cost_center = (
	# 			frappe.db.get_value("Project", source_parent.project, "cost_center")
	# 			or item.get("buying_cost_center")
	# 			or item_group.get("buying_cost_center")
	# 		)
	

	mapper = {
		"Stock Entry": {"doctype": "Stock Entry", "validation": {"docstatus": ["=", 1]}},
		# "Sales Taxes and Charges": {"doctype": "Sales Taxes and Charges", "add_if_empty": True},
		# "Sales Contributions and Incentives": {"doctype": "Sales Team", "add_if_empty": True},
	}

	if not skip_item_mapping:

		# def condition(doc):
		# 	# make_mapped_doc sets js `args` into `frappe.flags.args`
		# 	if frappe.flags.args and frappe.flags.args.delivery_dates:
		# 		if cstr(doc.delivery_date) not in frappe.flags.args.delivery_dates:
		# 			return False
		# 	return abs(doc.delivered_qty) < abs(doc.qty) and doc.delivered_by_supplier != 1

		mapper["Stock Entry Detail"] = {
			"doctype": "Stock Entry Detail",
			"field_map": {
				# "rate": "rate",
				"name": "name",
				"parent": "parent",
			},
			# "postprocess": update_item,
			# "condition": condition,
		}

	target_doc = get_mapped_doc("Stock Entry", source_name, mapper, target_doc, set_missing_values)

	target_doc.set_onload("ignore_price_list", True)

	return target_doc