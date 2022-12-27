

import frappe
from frappe import _
from frappe.utils import getdate
from datetime import datetime
from frappe.utils.background_jobs import  enqueue
from frappe.model.mapper import get_mapped_doc
from erpnext.selling.doctype.quotation.quotation import _make_customer
from frappe.utils import flt, getdate, nowdate
from erpnext.selling.doctype.sales_order.sales_order import make_purchase_order, is_product_bundle, set_delivery_date
from six import string_types
import json
from frappe.core.doctype.communication.email import make
from frappe.desk.form.load import get_attachments
from frappe.utils import get_url

DOMAINS = frappe.get_active_domains()

@frappe.whitelist()
def opportunity_notifiy(self, *args, **kwargs):
	if "IFI" in DOMAINS:
		# print('\n\n\n******** notifssssy')
		get_alert_dict(self)
		#reciever
		email_quotation(self, *args, **kwargs)
		# supplier_rfq_mail(self)
        
@frappe.whitelist()
def daily_opportunity_notify(self, *args, **kwargs ):
    # date_now =getdate()
    today = datetime.now().strftime('%Y-%m-%d')
    sql = f"""
        select name,contact_by,customer_name,contact_date,'Opportunity' as doctype from tabOpportunity to2 
		where CAST(contact_date AS DATE) ='{today}'
    """
    data = frappe.db.sql(sql,as_dict=1)
    for opprt in data:
        get_alert_dict(opprt)          

@frappe.whitelist()
def get_alert_dict(self):
    owner_name = self.contact_by
    customer_name = self.customer_name
    contact_date = self.contact_date
    notif_doc = frappe.new_doc('Notification Log')
    notif_doc.subject = f"{owner_name} Contact to {customer_name} at {contact_date}"
    notif_doc.for_user = owner_name
    notif_doc.type = "Mention"
    notif_doc.document_type = self.doctype
    notif_doc.document_name = self.name
    notif_doc.from_user = frappe.session.user
    notif_doc.insert(ignore_permissions=True)




@frappe.whitelist()
def email_quotation(self,*args, **kwargs): 
		receiver = frappe.db.get_value("User", self.contact_by, "email")
		if receiver:
			email_args = {
				"recipients": [receiver],
				"message": _("Quotation Appointement"),
				"subject": 'Quotation Appointement At Date'.format(self.contact_date),
                # "message": self.get_message(),
				# "attachments": [frappe.attach_print(self.doctype, self.name, file_name=self.name)],
				"reference_doctype": self.doctype,
				"reference_name": self.name
				}
			enqueue(method=frappe.sendmail, queue="short", timeout=300,now=True, is_async=True,**email_args)
		else:
			frappe.msgprint(_("{0}: Next Contatct By User Has No Mail, hence email not sent").format(self.contact_by))


@frappe.whitelist()
def email_supplier_invoice(self,*args, **kwargs): 
		receiver = frappe.db.get_value("Supplier", self.supplier, "email_id")
		if receiver:
			email_args = {
				"recipients": [receiver],
				"message": _("Please GET Notify "),
				"subject": 'Purchase Receipt - IN'.format(self.posting_date),
				# "attachments": [frappe.attach_print(self.doctype, self.name, file_name=self.name)],
				"reference_doctype": self.doctype,
				"reference_name": self.name
				}
			enqueue(method=frappe.sendmail, queue="short", timeout=300,now=True, is_async=True,**email_args)
		else:
			frappe.msgprint(_("{0}: Supplier ha no mail, hence email not sent").format(self.supplier))

@frappe.whitelist()
def create_furniture_installation_order(source_name, target_doc=None):
    doclist = get_mapped_doc("Sales Order", source_name, {
        "Sales Order": {
            "doctype": "Installations Furniture",
            "field_map": {
                "name": "sales_order",
                "customer": "customer"
            },
            "validation": {
                "docstatus": ["=", 1]
            }
        },
        "Sales Order Item": {
            "doctype": "Installation Furniture Item",
            "field_map": {
                "name":"ref_name",
                "item_code": "item_code",
                "item_name": "item_name",
                "qty": "qty",
                "rate": "rate",
                "amount": "amount",
                "delivery_date":"delivery_date",
            }
        }
    }, target_doc)
    
    return doclist
    

@frappe.whitelist()
def make_sales_order(source_name, target_doc=None):
	print('\n\n\n\n*****************')
	quotation = frappe.db.get_value(
		"Quotation", source_name, ["transaction_date", "valid_till"], as_dict=1
	)
	if quotation.valid_till and (
		quotation.valid_till < quotation.transaction_date or quotation.valid_till < getdate(nowdate())
	):
		frappe.throw(_("Validity period of this quotation has ended."))
	return _make_sales_order(source_name, target_doc)


def _make_sales_order(source_name, target_doc=None, ignore_permissions=False):
	customer = _make_customer(source_name, ignore_permissions)

	def set_missing_values(source, target):
		if customer:
			target.customer = customer.name
			target.customer_name = customer.customer_name
		if source.referral_sales_partner:
			target.sales_partner = source.referral_sales_partner
			target.commission_rate = frappe.get_value(
				"Sales Partner", source.referral_sales_partner, "commission_rate"
			)
		target.flags.ignore_permissions = ignore_permissions
		target.run_method("set_missing_values")
		target.run_method("calculate_taxes_and_totals")
		#Get the advance paid Journal Entries in Sales Invoice Advance
		if target.get("allocate_advances_automatically"):
			target.set_advances()

	def update_item(obj, target, source_parent):
		target.stock_qty = flt(obj.qty) * flt(obj.conversion_factor)

		if obj.against_blanket_order:
			target.against_blanket_order = obj.against_blanket_order
			target.blanket_order = obj.blanket_order
			target.blanket_order_rate = obj.blanket_order_rate

	doclist = get_mapped_doc(
		"Quotation",
		source_name,
		{
			"Quotation": {
                "doctype": "Sales Order",
                "field_map": {
                    "crean": "crean",
                    "crean_amount": "crean_amount",
					"allocate_advances_automatically":"allocate_advances_automatically"
                },
                "validation": 
                {"docstatus": ["=", 1]}
                },
			"Quotation Item": {
				"doctype": "Sales Order Item",
				"field_map": {"parent": "prevdoc_docname"},
				"postprocess": update_item,
			},
			"Sales Taxes and Charges": {"doctype": "Sales Taxes and Charges", "add_if_empty": True},
			"Sales Team": {"doctype": "Sales Team", "add_if_empty": True},
			"Payment Schedule": {"doctype": "Payment Schedule", "add_if_empty": True},
			"Sales Invoice Advance": {"doctype": "Sales Invoice Advance", "add_if_empty": True},
		},
		target_doc,
		set_missing_values,
		ignore_permissions=ignore_permissions,
	)

	# postprocess: fetch shipping address, set missing values
	doclist.set_onload("ignore_price_list", True)

	return doclist


@frappe.whitelist()
def override_make_purchase_order(source_name, selected_items=None, target_doc=None):
	if "IFI" in DOMAINS:
		if not selected_items:
			return

		if isinstance(selected_items, string_types):
			selected_items = json.loads(selected_items)

		items_to_map = [
			item.get("item_code")
			for item in selected_items
			if item.get("item_code") and item.get("item_code")
		]
		items_to_map = list(set(items_to_map))

		def set_missing_values(source, target):
			target.supplier = ""
			target.apply_discount_on = ""
			target.additional_discount_percentage = 0.0
			target.discount_amount = 0.0
			target.inter_company_order_reference = ""
			target.customer = ""
			target.customer_name = ""
			target.run_method("set_missing_values")
			target.run_method("calculate_taxes_and_totals")

		def update_item(source, target, source_parent):
			target.schedule_date = source.delivery_date
			target.qty = flt(source.qty) - (flt(source.ordered_qty) / flt(source.conversion_factor))
			target.stock_qty = flt(source.stock_qty) - flt(source.ordered_qty)
			target.project = source_parent.project

		def update_item_for_packed_item(source, target, source_parent):
			target.qty = flt(source.qty) - flt(source.ordered_qty)

		# po = frappe.get_list("Purchase Order", filters={"sales_order":source_name, "supplier":supplier, "docstatus": ("<", "2")})
		doc = get_mapped_doc(
			"Sales Order",
			source_name,
			{
				"Sales Order": {
					"doctype": "Purchase Order",
					"field_map": {
						"customer":"customer_so",
						
						},
					"field_no_map": [
						"address_display",
						"shipping_rule",
						"contact_display",
						"contact_mobile",
						"contact_email",
						"contact_person",
						"taxes_and_charges",
						"shipping_address",
						"terms",
					],
					"validation": {"docstatus": ["=", 1]},
				},
				"Sales Order Item": {
					"doctype": "Purchase Order Item",
					"field_map": [
						["name", "sales_order_item"],
						["parent", "sales_order"],
						["stock_uom", "stock_uom"],
						["uom", "uom"],
						["conversion_factor", "conversion_factor"],
						["delivery_date", "schedule_date"],
					],
					"field_no_map": [
						"rate",
						"price_list_rate",
						"item_tax_template",
						"discount_percentage",
						"discount_amount",
						"supplier",
						"pricing_rules",
					],
					"postprocess": update_item,
					"condition": lambda doc: doc.ordered_qty < doc.stock_qty
					and doc.item_code in items_to_map
					and not is_product_bundle(doc.item_code),
				},
				"Packed Item": {
					"doctype": "Purchase Order Item",
					"field_map": [
						["name", "sales_order_packed_item"],
						["parent", "sales_order"],
						["uom", "uom"],
						["conversion_factor", "conversion_factor"],
						["parent_item", "product_bundle"],
						["rate", "rate"],
					],
					"field_no_map": [
						"price_list_rate",
						"item_tax_template",
						"discount_percentage",
						"discount_amount",
						"supplier",
						"pricing_rules",
					],
					"postprocess": update_item_for_packed_item,
					"condition": lambda doc: doc.parent_item in items_to_map,
				},
			},
			target_doc,
			set_missing_values,
		)

		set_delivery_date(doc.items, source_name)

		return doc
	make_purchase_order(source_name, selected_items=None, target_doc=None)
	# print('\n\n\n\n/////*********')
	# print(source_name)

def supplier_rfq_mail(self,preview=False):
		# full_name = get_user_fullname(frappe.session["user"])
		# if full_name == "Guest":
		# 	full_name = "Administrator"

		# send document dict and some important data from suppliers row
		# to render message_for_supplier from any template
		doc_args = self.as_dict()
		doc_args.update({"party": self.party_name,"test":2222})

		args = {
			"message": frappe.render_template("hello from other side", doc_args),
			"rfq_link": get_link(self),
			"user_fullname": "abanoub moubir full name",
			"supplier_name": self.party_name,
			"supplier_salutation": "Dear Mx.",
		}

		subject = _("Request for Opportunity")
		template = "templates/emails/opportunity.html"
		sender = "abanoubmounir07@gmail.com"
		message = "message body for mail ---> %s" % args.get('rfq_link') #frappe.get_template(template).render(args)

		if preview:
			return message

		attachments = get_attachments2(self)

		send_email(self, sender, subject, message, attachments)

def send_email(self, sender, subject, message, attachments):
		make(
			subject=subject,
			content=message,
			recipients="abanoub.mounir9@gmail.com",
			sender=sender,
			attachments=attachments,
			send_email=True,
			doctype=self.doctype,
			name=self.name,
		)["name"]

		frappe.msgprint(_("Email Sent to Supplier {0}").format(self.party_name))

def get_attachments2(self,name=None):
		attachments = [d.name for d in get_attachments(self.doctype, self.name)]
		attachments.append(frappe.attach_print(self.doctype, self.name, doc=self))
		return attachments

def get_link(self):
		# RFQ link for supplier portal
		return get_url("/app/opportunity/" + self.name)

@frappe.whitelist()
def create_new_appointment_ifi(source_name, target_doc=None):
    doc = frappe.get_doc("Lead", source_name)
    appointment_doc = frappe.new_doc("Appointment")
    appointment_doc.customer_name = doc.lead_name
    appointment_doc.customer_phone_number = doc.get('phone_no1','') 
    appointment_doc.appointment_with = "Lead"
    appointment_doc.party = doc.name
    appointment_doc.customer_email = doc.email_id
    return appointment_doc

@frappe.whitelist()
def get_events(start, end, filters=None):
	"""Returns events for Gantt / Calendar view rendering.
	frappe
	:param start: Start date-time.
	:param end: End date-time.
	:param filters: Filters (JSON).
	"""
	from erpnext.controllers.queries import get_match_cond
	from frappe.desk.calendar import get_event_conditions
	filters = json.loads(filters)
	conditions = get_event_conditions("Installations Furniture", filters)
	events = []
	data = frappe.db.sql("""
		select
			`tabAppointment`.name as name,
			 `tabAppointment`.customer_name as cst,
			  `tabAppointment`.scheduled_time as start,
			 ADDTIME(`tabAppointment`.scheduled_time,'2:00:00') as end,
			 concat(`tabAppointment`.customer_name,'--',`tabAppointment`.scheduled_time )as description
		from
			`tabAppointment`
			{conditions}
		""".format(conditions=conditions),  as_dict=True,
		update={"allDay": 0},)
		
	# for row in data:
	# 	job_card_data = {
    #         "start": row.start,
    #         "planned_end_date": row.end,
    #         "name": row.name,
    #         "subject": row.customer,
    #         "color":'#D3D3D3',
    #     }
	# 	events.append(job_card_data)

	return data