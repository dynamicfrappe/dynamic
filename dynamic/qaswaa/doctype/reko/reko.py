# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
class reko(Document):
	pass



@frappe.whitelist()
def test():
	data = frappe._dict()
	data.name = 'pop'
	frappe.publish_realtime(
		"title realtime",
		dict(
			title=_("Opening Invoice Creation In Progress"),
			message=_("Creating real time 111"),
		),
		user=frappe.session.user,
	)

