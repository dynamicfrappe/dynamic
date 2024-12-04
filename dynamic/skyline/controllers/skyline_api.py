import frappe
from frappe import _

DOMAINS = frappe.get_active_domains()

@frappe.whitelist()
def validation_purchase(self , *args , **kwargs):
    validate_fast_purchase(self)
    validate_with_budget(self)



def validate_with_budget(self):
    if "Skyline" in DOMAINS:
        items = self.get("items")
        if items and self.first_approve == 0 and self.sec_approve ==0:
            for item in items:
                if item.rate > item.Budget:
                    frappe.throw(_("Item rate Cannot be greater than budget"))

def validate_fast_purchase(self):
    if "Skyline" in DOMAINS:
        fast_purchase_rate = frappe.get_doc("Buying Settings").fast_purchase_rate
        if fast_purchase_rate > 0:
            if self.fast_purchase:
                if self.grand_total > fast_purchase_rate:
                    frappe.throw(_("Supplier Quotation Cannot be greater than fast purchase"))

def set_total_amounts(self, *args, **kwargs):
    pass
    if "Skyline" in DOMAINS:
            
        total_contract = 0.0
        for contract in self.revised_contract_amount:
            if contract.amount:
                total_contract += float(contract.amount) or 0
        self.total_contracts = total_contract
        self.total_contract_amountt = (self.contract_amounts or 0) + total_contract

        # total_invoice = sum(invoice.amount for invoice in self.invoice_amounts if invoice.amount)
        # self.total_invoice_amount = total_invoice
        total_invoice = 0.0
        for invoice in self.invoice_amounts:
            if invoice.amount:
                total_invoice += float(invoice.amount) or 0
        self.total_invoice_amount = total_invoice

        # # total_paid = sum(paid.amount for paid in self.paid_amounts if paid.amount)
        # # self.total_paid_amount = total_paid
        total_paid = 0.0
        for paid in self.paid_amounts:
            if paid.amount:
                total_paid += float(paid.amount) or 0
        self.total_paid_amount = total_paid

        self.diff = self.total_invoice_amount - self.total_paid_amount

        total_cost = 0.0
        #for cost in self.revised_contract_budget:
        #   if cost.amount:
        #        total_cost += float(cost.amount) or 0
        self.total_rcb = total_cost
