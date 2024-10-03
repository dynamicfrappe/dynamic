import frappe
from frappe import _
DOMAINS = frappe.get_active_domains()

# @frappe.whitelist()
# def validate_reference_document(self):
#     if not self.reference_doctype or not self.reference_name:
#         # If reference_doctype or reference_name are missing, return False
#         return False
#     # Return True if both reference_doctype and reference_name are present
#     return True
   