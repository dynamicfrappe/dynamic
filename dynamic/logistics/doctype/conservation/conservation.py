# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Conservation(Document):
	@frappe.whitelist()
	def fetch_survey_template(self , survey):
		survey_doc = frappe.get_doc("Survey" , survey)
		for row in survey_doc.survey_template:
			self.append("survey_template" , row)
