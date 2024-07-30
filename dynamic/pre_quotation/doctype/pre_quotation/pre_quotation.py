# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe
from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt, getdate, nowdate

# from erpnext.controllers.selling_controller import SellingController

# form_grid_templates = {"items": "templates/form_grid/item_grid.html"}

class PreQuotation(Document):
	pass