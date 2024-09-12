import frappe
from frappe import _
DOMAINS = frappe.get_active_domains()

@frappe.whitelist()
def validate(self, method):
    if "YT Minds" in DOMAINS:
        validate_item_with_selling(self)
    
def validate_item_with_selling(self):
    if self.items:
        for item in self.items:
            item_code = item.get("item_code")
            price_of_sales_item = frappe.db.sql(f"""
                                                select 
                                                    so.name ,
                                                    soi.item_code,
                                                    soi.amount
                                                from 
                                                    `tabSales Order` so
                                                join
                                                    `tabSales Order Item` soi
                                                on
                                                    soi.parent = so.name
                                                where
                                                    soi.item_code = '{item_code}'
                                                ORDER BY
                                                    so.modified DESC
                                                 """,as_dict=1)
            if price_of_sales_item:
                amount = price_of_sales_item[0].get('amount')
                if item.amount > amount:
                    frappe.throw(_(f"""The Amount of {item.item_code} must be greater than {amount}"""))