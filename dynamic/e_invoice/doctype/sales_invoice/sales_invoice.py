from __future__ import unicode_literals
import frappe
from frappe.model.naming import make_autoname

def autoname(self,fun=''):
    series = "Tax-Inv-.DD.-.MM.-.YYYY.-.###." if getattr(self,'tax_auth' , 0) else self.naming_series
    self.name = make_autoname(series, doctype="Sales Invoice")
    frappe.msgprint(self.name)

