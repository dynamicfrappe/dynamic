import frappe
from frappe import _

DOMAINS = frappe.get_active_domains()

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
