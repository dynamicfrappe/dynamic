from erpnext.accounts.doctype.account.account import get_account_currency
import frappe

from frappe.utils import add_days, nowdate, today
from dynamic.terra.doctype.payment_entry.payment_entry import get_party_details
from frappe.model.mapper import get_mapped_doc
from frappe.model.utils import get_fetch_values
from frappe.utils import add_days, cint, cstr, flt, get_link_to_form, getdate, nowdate, strip_html
from six import string_types
from frappe.utils import now
from erpnext.stock.utils import get_stock_balance
from dynamic.api import validate_purchase_recipt, check_email_setting_in_stock_setting, check_pr_reservation

Domains = frappe.get_active_domains()

def purchase_reciept_before_submit(doc,*args,**kwargs):
    frappe.throw('test')
    if 'Gebco' in Domains:
        validate_purchase_recipt(doc)
    if 'Terra' in Domains:
        check_email_setting_in_stock_setting(doc)
        #check if PR has Reservation & reserve over warehouse
        check_pr_reservation(doc)

@frappe.whitelist()
def get_iem_sub_uom(item_code,uom,qty):
	item  = frappe.get_doc("Item",item_code)
	# if len(item.uoms) >=1:
	#     if item.uoms[1].uom == uom:
	#         return {
	#         "sub_uom":item.uoms[1].uom,
	#         "sub_uom_conversation_factor":item.uoms[1].conversion_factor,
	#         "qty_as_per_sub_uom": qty
	#     }
	#     return {
	#         "sub_uom":item.uoms[1].uom,
	#         "sub_uom_conversation_factor":item.uoms[1].conversion_factor,
	#         "qty_as_per_sub_uom": float(qty or 0) / float(item.uoms[1].conversion_factor or 0)
	#     }
	# return {
	#         "sub_uom":"",
	#         "sub_uom_conversation_factor":0,
	#         "qty_as_per_sub_uom": 0
	#     }
	for u in item.uoms:
		if u.is_sub_uom:
			if u.uom !=uom:
				return {
					"sub_uom":u.uom,
					"sub_uom_conversation_factor":u.conversion_factor,
					"qty_as_per_sub_uom": float(qty or 0) / float(u.conversion_factor or 0)
				}

			if u.uom == uom :
				return {
					"sub_uom":u.uom,
					"sub_uom_conversation_factor":u.conversion_factor,
					"qty_as_per_sub_uom": qty
				}

	return {
			"sub_uom":"",
			"sub_uom_conversation_factor":0,
			"qty_as_per_sub_uom": 0
		}



# material request type ------------> purchase
# validate if no item   ------------> validation error 
@frappe.whitelist()
def create_sales_order_from_opportunity(source_name, target_doc=None):
	source_doc = frappe.get_doc("Opportunity",source_name)
	doc = frappe.new_doc("Sales Order")
	if source_doc.opportunity_from == "Customer":
		doc.customer = source_doc.party_name
		doc.opportunity = source_doc.name
		doc.source = source_doc.source
	if len(source_doc.items)> 0:
		for item in source_doc.items:
			item_doc = frappe.get_doc("Item",item.item_code)
			doc.append("items",{
				"item_code"     : item.item_code,
				"qty"           : item.qty,
				"item_name"     : item.item_name,
				"description"   : item.item_name,
				"uom"           : item_doc.stock_uom,
				"stock_uom"     : item_doc.stock_uom
			})
	source_doc.db_set('status','Converted')
	return doc

@frappe.whitelist()
def create_material_request_from_opportunity(source_name, target_doc=None):
	source_doc = frappe.get_doc("Opportunity",source_name)
	doc = frappe.new_doc("Material Request")
	doc.purpose = "Purchase"
	doc.customer_name = source_doc.customer_name if source_doc.customer_name else ''
	doc.opportunity = source_doc.name  
	if len(source_doc.items)> 0:
		for item in source_doc.items:
			item_doc = frappe.get_doc("Item",item.item_code)
			doc.append("items",{
				"item_code"     : item.item_code,
				"qty"           : item.qty,
				"item_name"     : item.item_name,
				"description"   : item.item_name,
				"uom"           : item_doc.stock_uom,
				"stock_uom"     : item_doc.stock_uom,
				"schedule_date" : today()
			})
	return doc




@frappe.whitelist()
def get_quotation_item(quotation,*args,**Kwargs):
	doc = frappe.get_doc("Quotation",quotation)
	return doc.items
	
@frappe.whitelist()
def get_payment_entry_quotation(source_name):
	qutation_doc = frappe.get_doc('Quotation',source_name)

	party_type = qutation_doc.quotation_to
	party = qutation_doc.party_name

	if qutation_doc.quotation_to == "Lead" :
		party_type = "Customer"
		party = frappe.db.get_value("Customer" , {"lead_name":qutation_doc.party_name},'name')
		
		if not party :
			from dynamic.terra.doctype.quotation.quotation import make_customer
			customer = make_customer(source_name,ignore_permissions=True)
			if customer :
				party = customer.name



	from erpnext.accounts.doctype.sales_invoice.sales_invoice import get_bank_cash_account
	# from erpnext.accounts.party import get_party_account
	pe = frappe.new_doc("Payment Entry")
	pe.payment_type = "Receive"
	pe.mode_of_payment = "Cash"
	pe.company = qutation_doc.company
	pe.paid_to = (get_bank_cash_account(pe.mode_of_payment,pe.company) or {}).get("account")
	if pe.paid_to :
		pe.paid_to_account_currency = get_account_currency(pe.paid_to)
	pe.party_type = party_type
	pe.party = party
	pe.party_name = qutation_doc.customer_name

	pe.paid_amount = (qutation_doc.base_rounded_total or qutation_doc.base_grand_total) - (getattr(qutation_doc,'advance_paid',0))
	pe.received_amount = pe.paid_amount
	pe.received_amount_after_tax = pe.paid_amount
	# cash_detail = get_all_apyment_for_quotation(source_name)
	#modify to outstand amount
	row = pe.append('references',{})
	row.reference_doctype = "Quotation"
	row.reference_name = source_name
	
	row.outstanding_amount = pe.paid_amount
	row.allocated_amount = pe.paid_amount
	# if cash_detail!= False :
		# pe.paid_amount = cash_detail.get("outstand")
		# row.outstanding_amount = cash_detail.get("outstand") #modify to outstand amount
	cst_account = get_party_details(company=qutation_doc.company,date=None,
	party_type=party_type, 
	party=party,
	cost_center=None)
	pe.part_balance = cst_account.get('party_balance')
	pe.paid_from = cst_account.get('party_account')
	# pe.paid_from = get_party_account(pe.party_type,pe.party , pe.company)#cst_account.get('party_account')
	pe.paid_from_account_currency = cst_account.get('party_account_currency')
	pe.paid_from_account_balance = cst_account.get('account_balance')
	return pe



def get_all_apyment_for_quotation(qutation_name):
	sql=f'''
			select tper.parent,tper.reference_name ,tper.total_amount, 
			IFNULL(SUM(tper.allocated_amount),0) total_paid,
			(tper.total_amount-IFNULL(SUM(tper.allocated_amount),0))outstand
			from `tabPayment Entry Reference` tper
			where tper.reference_name='{qutation_name}' 
			GROUP by tper.reference_name
	'''
	data = frappe.db.sql(sql,as_dict=1)
	if len(data) > 0 :

		return data[0]
	else :
		return False


@frappe.whitelist()
def add_paid_amount(payment,*args,**Kwargs):
	if 'Terra' in Domains:
		if(payment.references[0].get('reference_doctype')=='Quotation'):
			outstand_amount = frappe.db.get_value('Quotation', payment.references[0].get('reference_name'),'outstand_amount') or 0
			frappe.db.set_value('Quotation', payment.references[0].get('reference_name'),'outstand_amount',outstand_amount + payment.total_allocated_amount )
		

@frappe.whitelist()
def cancel_amount_quotation(payment,*args,**Kwargs):
	if 'Terra' in Domains:
		if(payment.references[0].get('reference_doctype')=='Quotation'):
			outstand_amount = frappe.db.get_value('Quotation', payment.references[0].get('reference_name'),'outstand_amount') or 0
			frappe.db.set_value('Quotation', payment.references[0].get('reference_name'),'outstand_amount',outstand_amount - payment.total_allocated_amount )
		#     frappe.errprint(f'outstand_amount-->{outstand_amount}')
		#     frappe.errprint(f'payment.total_allocated_amount-->{payment.total_allocated_amount}')
		# ...

@frappe.whitelist()
def submit_supplier_quotation(doc ,*args ,**kwargs) :
	if 'Terra' in Domains:
		from dynamic.terra.doctype.supplier_quotation.supplier_quotation import submit_supplier_quotation as tera_submit_quotation
		tera_submit_quotation(doc) 





@frappe.whitelist()
def create_action_doc(source_name ,target_doc=None ):
	doctype = frappe.flags.args.doctype
	# source_doc = frappe.get_doc(doctype,docname)
	target_doc = frappe.new_doc("Actions")
	target_doc.customer_type = doctype
	target_doc.customer = source_name
	return target_doc

@frappe.whitelist()
def get_item_group_brand(doctype, txt, searchfield, start, page_len, filters):
	condition = ' 1=1 '
	item_group = filters.get("item_group") or ""
	brand = filters.get("brand") or ""
	if item_group:
		condition += f'AND item.item_group="{item_group}" '
	if brand:
		condition += f'AND item.brand="{brand}" '

	search_txt = "%%%s%%" % txt
	data = frappe.db.sql(
		f"""SELECT item.name,item.item_code,item.item_group,item.brand
		FROM `tabItem` item
			where {condition}
			and (item.name like '{search_txt}' )"""
	)
	return data

@frappe.whitelist()
def create_cst_appointment(source_name ,target_doc=None):
	source_doc = frappe.get_doc("Customer",source_name)
	target_doc = frappe.new_doc("Appointment")
	target_doc.customer_name = source_doc.customer_name
	target_doc.scheduled_time = now()
	return target_doc



@frappe.whitelist()
def get_items(
	warehouse, posting_date, posting_time, company, item_code=None, ignore_empty_stock=False
):
	ignore_empty_stock = cint(ignore_empty_stock)
	items = [frappe._dict({"item_code": item_code, "warehouse": warehouse})]

	if not item_code:
		items = get_items_for_stock_reco(warehouse, company)

	res = []
	itemwise_batch_data = get_itemwise_batch(warehouse, posting_date, company, item_code)

	for d in items:
		if d.item_code in itemwise_batch_data:
			valuation_rate = get_stock_balance(
				d.item_code, d.warehouse, posting_date, posting_time, with_valuation_rate=True
			)[1]

			for row in itemwise_batch_data.get(d.item_code):
				if ignore_empty_stock and not row.qty:
					continue

				args = get_item_data(row, row.qty, valuation_rate)
				res.append(args)
		else:
			stock_bal = get_stock_balance(
				d.item_code,
				d.warehouse,
				posting_date,
				posting_time,
				with_valuation_rate=True,
				with_serial_no=cint(d.has_serial_no),
			)
			qty, valuation_rate, serial_no = (
				stock_bal[0],
				stock_bal[1],
				stock_bal[2] if cint(d.has_serial_no) else "",
			)

			if ignore_empty_stock and not stock_bal[0]:
				continue

			args = get_item_data(d, qty, valuation_rate, serial_no)

			res.append(args)

	return res

def get_items_for_stock_reco(warehouse, company):
	lft, rgt = frappe.db.get_value("Warehouse", warehouse, ["lft", "rgt"])
	# frappe.throw('test')
	items = frappe.db.sql(
		f"""
		select
			i.name as item_code, i.item_name, bin.warehouse as warehouse, i.has_serial_no, i.has_batch_no,
			i.brand,i.item_group
		from
			tabBin bin, tabItem i
		where
			i.name = bin.item_code
			and IFNULL(i.disabled, 0) = 0
			and i.is_stock_item = 1
			and i.has_variants = 0
			and exists(
				select name from `tabWarehouse` where lft >= {lft} and rgt <= {rgt} and name = bin.warehouse
			)
	""",
		as_dict=1,
	)

	items += frappe.db.sql(
		"""
		select
			i.name as item_code, i.item_name, id.default_warehouse as warehouse, i.has_serial_no, i.has_batch_no
		from
			tabItem i, `tabItem Default` id
		where
			i.name = id.parent
			and exists(
				select name from `tabWarehouse` where lft >= %s and rgt <= %s and name=id.default_warehouse
			)
			and i.is_stock_item = 1
			and i.has_variants = 0
			and IFNULL(i.disabled, 0) = 0
			and id.company = %s
		group by i.name
	""",
		(lft, rgt, company),
		as_dict=1,
	)

	# remove duplicates
	# check if item-warehouse key extracted from each entry exists in set iw_keys
	# and update iw_keys
	iw_keys = set()
	items = [
		item
		for item in items
		if [
			(item.item_code, item.warehouse) not in iw_keys,
			iw_keys.add((item.item_code, item.warehouse)),
		][0]
	]

	return items


def get_item_data(row, qty, valuation_rate, serial_no=None):
	return {
		"item_code": row.item_code,
		"warehouse": row.warehouse,
		"qty": qty,
		"item_name": row.item_name,
		"valuation_rate": valuation_rate,
		"current_qty": qty,
		"current_valuation_rate": valuation_rate,
		"current_serial_no": serial_no,
		"serial_no": serial_no,
		"batch_no": row.get("batch_no"),
		"brand": row.get("brand"),
		"item_group": row.get("item_group"),
	}

def get_itemwise_batch(warehouse, posting_date, company, item_code=None):
	from erpnext.stock.report.batch_wise_balance_history.batch_wise_balance_history import execute

	itemwise_batch_data = {}

	filters = frappe._dict(
		{"warehouse": warehouse, "from_date": posting_date, "to_date": posting_date, "company": company}
	)

	if item_code:
		filters.item_code = item_code

	columns, data = execute(filters)

	for row in data:
		itemwise_batch_data.setdefault(row[0], []).append(
			frappe._dict(
				{
					"item_code": row[0],
					"warehouse": warehouse,
					"qty": row[8],
					"item_name": row[1],
					"batch_no": row[4],
				}
			)
		)

	return itemwise_batch_data