import frappe
from frappe import _
from frappe.utils.user import get_users_with_role
from erpnext import get_default_company
from frappe.desk.reportview import get_filters_cond, get_match_cond
from frappe import _
from erpnext.controllers.queries import get_fields
from frappe.utils import get_host_name, escape_html, get_url
from erpnext.accounts.doctype.pos_invoice.pos_invoice import get_bin_qty
from collections import defaultdict


DOMAINS = frappe.get_active_domains()


@frappe.whitelist()
def alert_cheque_date():
    if "Cheques" in DOMAINS:
        company = get_default_company()
        get_role = frappe.db.get_value("Company", company, "notification_cheque_role")
        if get_role:
            cheque_data = frappe.db.sql(
                """
			SELECT cheque_no,cheque_date 
			FROM `tabCheque Table` 
			WHERE cheque_date < CURDATE() AND (DATE_ADD(cheque_date, INTERVAL 2 DAY)=CURDATE());
			""",
                as_dict=1,
            )
            cheque_list = [row["cheque_no"] for row in cheque_data]
            msg = cheque_list
            subject = "Cheque Notification"
            # send_mail_by_role(get_role,msg,subject)
            sender = frappe.session.user
            recip_list = get_users_with_role(get_role)
            subject = f"Alert For all Cheque Should Be Paid in 2 Days : {cheque_list}"
            get_alert_dict(company, sender, recip_list, subject)

# @frappe.whitelist()
def send_mail_by_role(role, msg, subject):
    try:
        recip_list = get_users_with_role(role)
        if recip_list:
            email_args = {
                "recipients": recip_list,
                "sender": None,
                "subject": subject,
                "message": msg,
                "now": True,
            }
            if not frappe.flags.in_test:
                frappe.enqueue(
                    method=frappe.sendmail,
                    queue="short",
                    timeout=500,
                    is_async=True,
                    **email_args,
                )
            else:
                frappe.sendmail(**email_args)
            return email_args
    except Exception as ex:
        print("exception", str(ex))

		

@frappe.whitelist()
def get_alert_dict(doc, sender, reciever, subject, **kwargs):
    for user in reciever:
        notif_doc = frappe.new_doc("Notification Log")
        notif_doc.subject = subject
        notif_doc.for_user = user
        notif_doc.type = "Alert"
        notif_doc.document_type = ""
        notif_doc.document_name = ""  # self.name
        notif_doc.from_user = frappe.session.user or sender
        notif_doc.insert(ignore_permissions=True)



# @frappe.whitelist()
# # @frappe.validate_and_sanitize_search_inputs
# def get_supplier_by_code(doctype, txt, searchfield, start, page_len, filters):
#     frappe.throw("test")
#     sales_order = filters.get("sales_order") or ''
#     search_txt = "%%%s%%" % txt

#     return frappe.db.sql(f"""select item.name , item.item_name
#                     from tabItem item
#                     inner join `tabSales Order Item` child
#                         on  child.item_code = item.name
#                     where child.parent = '{sales_order}'
#                     and (item.name like '{search_txt}' or item.item_name like '{search_txt}' )""")

@frappe.whitelist()
def get_supplier_by_code(
    doctype, txt, searchfield, start, page_len, filters, as_dict=False
):
    doctype = "Supplier"
    supp_master_name = frappe.defaults.get_user_default("supp_master_name")
    # frappe.throw("test55")
    fields = ["name"]
    if supp_master_name != "Supplier Name":
        fields.append("supplier_name")

    fields = get_fields(doctype, fields)
    fields.append("supplier_code")
    return frappe.db.sql(
        """select {field} from `tabSupplier`
		where docstatus < 2
			and ({key} like %(txt)s
			or supplier_name like %(txt)s or supplier_code like %(txt)s)
			  and disabled=0
			and (on_hold = 0 or (on_hold = 1 and CURDATE() > release_date))
			{mcond}
		order by
			if(locate(%(_txt)s, name), locate(%(_txt)s, name), 99999),
			if(locate(%(_txt)s, supplier_name), locate(%(_txt)s, supplier_name), 99999),
			idx desc,
			name, supplier_name
		limit %(start)s, %(page_len)s """.format(
            **{
                "field": ", ".join(fields),
                "key": searchfield,
                "mcond": get_match_cond(doctype),
            }
        ),
        {
            "txt": "%%%s%%" % txt,
            "_txt": txt.replace("%", ""),
            "start": start,
            "page_len": page_len,
        },
        as_dict=as_dict,
    )


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def customer_query_custom(
    doctype, txt, searchfield, start, page_len, filters, as_dict=False
):
    # frappe.throw("test")ظ
    doctype = "Customer"
    conditions = []
    cust_master_name = frappe.defaults.get_user_default("cust_master_name")

    fields = ["name"]
    if cust_master_name != "Customer Name":
        fields.append("customer_name")

    fields = get_fields(doctype, fields)
    searchfields = frappe.get_meta(doctype).get_search_fields()
    searchfields.append("customer_code")
    searchfields = " or ".join(field + " like %(txt)s" for field in searchfields)

    return frappe.db.sql(
        """select {fields} from `tabCustomer`
		where docstatus < 2
			and ({scond}) and disabled=0
			{fcond} {mcond}
		order by
			if(locate(%(_txt)s, name), locate(%(_txt)s, name), 99999),
			if(locate(%(_txt)s, customer_name), locate(%(_txt)s, customer_name), 99999),
			idx desc,
			name, customer_name
		limit %(start)s, %(page_len)s""".format(
            **{
                "fields": ", ".join(fields),
                "scond": searchfields,
                "mcond": get_match_cond(doctype),
                "fcond": get_filters_cond(doctype, filters, conditions).replace(
                    "%", "%%"
                ),
            }
        ),
        {
            "txt": "%%%s%%" % txt,
            "_txt": txt.replace("%", ""),
            "start": start,
            "page_len": page_len,
        },
        as_dict=as_dict,
    )


@frappe.whitelist()
def get_options(doc, arg=None):
    if frappe.get_meta("Sales Invoice").get_field("naming_series"):
        return frappe.get_meta("Sales Invoice").get_field("naming_series").options


def deals_after_insert(doc, *args, **kwargs):
    if "Master Deals" in DOMAINS:
        if doc.attached_to_doctype == "Item" and doc.attached_to_name != None:
            item_attach = frappe.db.get_list(
                "File",
                filters={
                    "attached_to_doctype": "Item",
                    "attached_to_name": doc.attached_to_name,
                },
                fields=["name"],
            )
            if len(item_attach) == 1:
                frappe.db.set_value("Item", doc.attached_to_name, "image", doc.file_url)


@frappe.whitelist()
def QRcode_Customer_data(doc):
	server_url = get_host_name() #'192.168.1.11' #
	customer_name=doc.name
	return f'http://{server_url}/app/customer/{customer_name}'
	
	
def escape_html_demo(text):
	if not isinstance(text, str):
		return text

	html_escape_table = {
		"&": "&amp;",
		'"': "&quot;",
		"'": "&apos;",
		">": "&gt;",
		"<": "&lt;",
        "+": "&amp;",
        # " ": "%20",
        " ": ";",
	}

	return "".join(html_escape_table.get(c, c) for c in text)


# @frappe.whitelist()
# def create_cst(cst_name):
# 	new_doc = frappe.new_doc('Sales Invoice')
# 	new_doc.customer = cst_name
# 	new_doc.run_method("set_missing_values")
# 	print(f'\n\n=new_doc=>{new_doc.__dict__}')
# 	print(f'\n\n=new_doc=>{new_doc.name}')
# 	return new_doc.name /home/beshoy/Dynamic-13/tera/frappe-tera/apps/dynamic/dynamic/master_deals/master_deals_api.py
#from dynamic.master_deals.master_deals_api import get_current_item_available_qty

@frappe.whitelist()
def get_current_item_available_qty( item , s_warehouse ,purpose = None  ,doc=None,factor = None) :
	"""
	Allowed documents ['Delivery Note' , 'Stock Entry']
	params item        -- item name --string
			s_warehouse  -- warehouse name -- String  
			purpose      -- stock entry type should be one off accepted types 
			doc          -- current doctype name 
				
	""" 
	if purpose :
		try :
			entry_type =  frappe.get_doc("Stock Entry Type" ,purpose).purpose 
			purpose = entry_type
		except Exception as e:
			print(e)				
			purpose = entry_type
	if not purpose :
					purpose ="Material Issue"
	if 'Master Deals' in DOMAINS:
			valid_qty = 0 
			if purpose in ["Material Issue" ,
			"Material Transfer" , 
			"Material Transfer for Manufacture" ,
			"Send to Subcontractor"] :
				actual_qty = get_bin_qty(item ,s_warehouse )
				# available Qty in current Uom  
				if (float(actual_qty or 0 ) != 0 )and (factor and factor != 1) :
					actual_qty = float(actual_qty) / float(factor or 0)
				qty =  get_item_sum_draft_qty(item , s_warehouse , document_name=doc)   
				valid_qty = (float (actual_qty or 0) -float(qty or 0) )                              		
			return valid_qty

def get_item_sum_draft_qty(item ,s_warehouse , document_name =None):
	"""
   Allowed documents ['Delivery Note' , 'Stock Entry']
   params item        -- item name --string
          s_warehouse -- warehouse name -- String  
          document    -- current doctype name 
            
	"""
	total_draft_qty = 0
	#get sum item qty in stock entry 
	stock_entry_allowed_types =""" ("Material Issue" , "Material Transfer" , 
			   						 "Material Transfer for Manufacture" , "Send to Subcontractor")"""
	stock_entry_sql = f"""
								SELECT SUM(a.transfer_qty)  as valid_qty FROM `tabStock Entry Detail` a
								inner Join `tabStock Entry` b 
								on a.parent = b.name
								WHERE b.docstatus=0  AND a.item_code = '{item}'  
								AND a.s_warehouse = '{s_warehouse}' 
								AND b.stock_entry_type in (
										SELECT name from `tabStock Entry Type` WHERE purpose
										in {stock_entry_allowed_types}
										)
							"""
	#get sum item qty in Delivery Note
	delivery_note_sql = f"""
     SELECT SUM(a.stock_qty) as valid_qty FROM `tabDelivery Note Item` a
     INNER JOIN `tabDelivery Note` b 
     on a.parent = b.name
	  WHERE b.docstatus=0  AND a.item_code = '{item}'
     AND 
	  a.warehouse = '{s_warehouse}' 
     """
	
	# if current document saved before remove local item from the submission  
	if document_name :
		stock_entry_sql = stock_entry_sql +f"AND b.name NOT IN ('{document_name}')"
		delivery_note_sql = delivery_note_sql +f"AND b.name NOT IN ('{document_name}')"
	stock_entry_data = frappe.db.sql(stock_entry_sql , as_dict=1)
	delivery_note_data = frappe.db.sql(delivery_note_sql , as_dict=1)
	if stock_entry_data and len(stock_entry_data) > 0 :
				total_draft_qty +=  float( stock_entry_data[0].get("valid_qty") or 0)
	if delivery_note_data and len(delivery_note_data) > 0 :
				total_draft_qty +=  float( delivery_note_data[0].get("valid_qty") or 0 )
	return total_draft_qty
def delivery_note_validate_item_qty(doc, *args):
    if "Master Deals" in DOMAINS:
        for item in doc.items:
            act_qty = get_bin_qty(item.item_code, item.warehouse)
            reqd_qty = float(item.qty or 0) * float(item.conversion_factor or 1)
            if float(act_qty) < float(reqd_qty):
                frappe.throw(
                    _(
                        f"Item '{item.item_code}'  Has No Qty In Warehouse '{item.warehouse}'"
                    )
                )


def stock_entry_validate_item_qty(doc, *args):
    if "Master Deals" in DOMAINS:
        entry_type = frappe.get_doc("Stock Entry Type", doc.stock_entry_type)
        if entry_type.purpose in [
            "Material Issue",
            "Material Transfer",
            "Material Transfer for Manufacture",
            "Send to Subcontractor",
        ]:
            for item in doc.items:
                act_qty = get_bin_qty(item.item_code, item.s_warehouse)
                reqd_qty = float(item.qty or 0) * float(item.conversion_factor or 1)
                if float(act_qty) < float(reqd_qty):
                    frappe.throw(
                        _(
                            f" <b>Item '{item.item_code}'</b>  hasn't this qty in warehouse <b>'{item.s_warehouse}'</b>"
                        )
                    )



@frappe.whitelist()
def get_last_doctype(doc_type=None):
	if 'Master Deals' in DOMAINS:
		return frappe.get_last_doc(doc_type)
        

@frappe.whitelist()
def get_avail_qty_in_draft_delivery(self, *args):
	if "Master Deals" in DOMAINS:
		# add stock setting flage
		if frappe.db.get_single_value("Selling Settings", "check_qty"):
			for item in self.items :
				if item.available_qty < item.stock_qty :
					frappe.throw(_(f""" item {item.item_code} Has Not Enough qty 
										in warehouse {item.warehouse} \n Current Qty = {item.available_qty} 
.
																				And required qty {item.stock_qty}"""))
                                        


@frappe.whitelist()
def get_avail_qty_in_draft_stock_entry(self, *args):
	if "Master Deals" in DOMAINS:
		# add stock setting flage
		if frappe.db.get_single_value("Selling Settings", "check_qty"):
			for item in self.items :
				if item.available_qty < item.transfer_qty :
					frappe.throw(_(f""" item {item.item_code} Has Not Enough qty 
										in warehouse {item.s_warehouse} \n Current Qty = {item.available_qty} 
																				And required qty {item.transfer_qty}"""))
@frappe.whitelist()
def get_avail_qty_in_draft_stock_delivry_2(doc, *args):
   
        
    if "Master Deals" in DOMAINS:
        # add stock setting flage
        if frappe.db.get_single_value("Selling Settings", "check_qty"):
            items = ",".join(f"'{(item.item_code)}'" for item in doc.items)
            # frappe.errprint(f'data=>{items}=\n\n')

            stock_sql = f"""
				SELECT `tabStock Entry Detail`.item_code ,`tabStock Entry Detail`.s_warehouse as warehouse
				,SUM(`tabStock Entry Detail`.qty) as prev_qty
				FROM `tabStock Entry`
				INNER JOIN `tabStock Entry Type`
				ON `tabStock Entry Type`.name=`tabStock Entry`.stock_entry_type 
				INNER JOIN `tabStock Entry Detail`  
				ON `tabStock Entry Detail`.parent=`tabStock Entry`.name
				WHERE `tabStock Entry Type`.purpose IN ('Material Transfer','Material Issue')
				AND `tabStock Entry Detail`.item_code 
				IN ({items})
				AND `tabStock Entry`.docstatus=0 AND `tabStock Entry Detail`.qty>0
				GROUP BY  `tabStock Entry Detail`.item_code ,`tabStock Entry Detail`.s_warehouse 
			"""
            stock_data = frappe.db.sql(stock_sql, as_dict=1)
            frappe.errprint(f"stock_data=>{stock_data}=\n\n")
            dn_sql = f"""
				SELECT `tabDelivery Note Item`.item_code ,`tabDelivery Note Item`.warehouse
				,SUM(`tabDelivery Note Item`.qty) as prev_qty 
				FROM `tabDelivery Note`
				INNER JOIN `tabDelivery Note Item` 
				ON `tabDelivery Note Item`.parent=`tabDelivery Note`.name
				WHERE `tabDelivery Note`.docstatus=0 AND `tabDelivery Note Item`.qty>0
				AND`tabDelivery Note Item`.item_code 
				IN ({items})
				GROUP BY `tabDelivery Note Item`.item_code ,`tabDelivery Note Item`.warehouse  
			"""
            dn_data = frappe.db.sql(dn_sql, as_dict=1)
            # frappe.errprint(f'dn_data=>{dn_data}=\n\n')
            # Merge lists x and y
            combined_list = stock_data + dn_data
            # Create a defaultdict to store the sums
            sums = defaultdict(int)
            # Sum 'age' values based on mutual 'id' and 'name' keys
            for item in combined_list:
                key = (item["item_code"], item["warehouse"])
                sums[key] += item["prev_qty"]
            # Reconstruct the list of dictionaries with summed 'age' values
            result = [
                {"item_code": key[0], "warehouse": key[1], "prev_qty": value}
                for key, value in sums.items()
            ]
            # frappe.errprint(f'result=>{result}=\n\n')
            # frappe.throw('test')
            warehouse = ""
            if doc.doctype == "Stock Entry":
                warehouse = "s_warehouse"
            else:
                warehouse = "warehouse"

            for item_dic in result:
                actual_bin_qty = frappe.db.get_value(
                    "Bin",
                    {
                        "item_code": item_dic.get("item_code"),
                        "warehouse": item_dic.get("warehouse"),
                    },
                    ["actual_qty"],
                )
                for row in doc.items:
                    if row.get("item_code") == item_dic.get("item_code") and row.get(
                        warehouse
                    ) == item_dic.get("warehouse"):
                        if (actual_bin_qty - item_dic.get("prev_qty") < row.qty) and  (actual_bin_qty - item_dic.get("prev_qty") != row.qty):
                            frappe.throw(
                                _(
                                    f"""Warehouse {item_dic.get('warehouse')}  Has No Qty For Item Code '{row.item_code}' <br>
							Actual QTY {actual_bin_qty} AND Reserved {item_dic.get('prev_qty')}
						"""
                                )
                            )
