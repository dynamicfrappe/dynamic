
import copy
import frappe
from frappe.utils import get_site_url
from frappe.utils.data import get_url
from frappe.utils.jinja import render_template
from frappe.utils.pdf import get_pdf

@frappe.whitelist(allow_guest=True)
def download_pdf(name, doctype = "Sales Invoice" , format="Invoice Tax", doc=None, no_letterhead=0):
	doc = frappe.get_doc("Sales Invoice", name)
	html =  render_template("dynamic_accounts/print_format/invoice_tax/invoice_tax.html", {"doc" : doc} , is_path=1)
	frappe.local.response.filename = "{name}.pdf".format(name=name.replace(" ", "-").replace("/", "-"))
	frappe.local.response.filecontent = get_pdf(html)
	frappe.local.response.type = "pdf"



@frappe.whitelist(allow_guest=True)
def get_invoice_tax_data(doc):
	doc = frappe.get_doc("Sales Invoice", doc)
	total_discount_amount = sum([(x.discount_amount or 0) for x in doc.items])
	total_tax_amount = sum([(x.tax_amount or 0) for x in doc.items])
	# server_url = frappe.local.conf.host_name or frappe.local.conf.hostname
	server_url = get_url()
	# frappe.msgprint(server_url)

	return {
		"total_discount_amount" : total_discount_amount ,
		"total_tax_amount" : total_tax_amount ,
		"server_url" : server_url ,
	}




