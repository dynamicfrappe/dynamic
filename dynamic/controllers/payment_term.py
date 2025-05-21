import frappe


def validate(self):
    if self.disable_on and not self.flags.in_insert:
        old_doc = frappe.get_doc(self.doctype, self.name)
        if old_doc.disable_on != self.disable_on:
            frappe.throw("You cannot change 'Disable On' after saving.")