from dynamic.api import get_item_price
import frappe
from frappe.model.mapper import get_mapped_doc
import requests 
from werkzeug.wrappers import Response
#dynamic.elevana.api
import json

from frappe.utils.data import nowdate
from frappe import _
from erpnext import get_company_currency, get_default_company, get_default_cost_center
import urllib.parse

def elevana_lead_before_insert(doc, fun=''):
    set_sales_person(doc)


def set_sales_person(doc):
    # frappe.msgprint('ss')
    if not doc.sales_person:
        employee = frappe.db.get_value(
            "Employee", {'user_id': frappe.session.user}, 'name')
        if employee:
            sales_person = emp = frappe.db.get_value(
                "Sales Person", {'employee': employee}, 'name')
            if sales_person:
                doc.sales_person = sales_person


@frappe.whitelist()
def make_quotation(source_name, target_doc=None):
    def set_missing_values(source, target):
        _set_missing_values(source, target)

    target_doc = get_mapped_doc(
        "Lead",
        source_name,
        {"Lead": {"doctype": "Quotation", "field_map": {"name": "party_name"}}},
        target_doc,
        set_missing_values,
    )
    target_doc.quotation_to = "Lead"
    target_doc.run_method("set_missing_values")
    target_doc.run_method("set_other_charges")
    target_doc.run_method("calculate_taxes_and_totals")

    return target_doc


def _set_missing_values(source, target):
    address = frappe.get_all(
        "Dynamic Link",
        {
            "link_doctype": source.doctype,
            "link_name": source.name,
            "parenttype": "Address",
        },
        ["parent"],
        limit=1,
    )

    contact = frappe.get_all(
        "Dynamic Link",
        {
            "link_doctype": source.doctype,
            "link_name": source.name,
            "parenttype": "Contact",
        },
        ["parent"],
        limit=1,
    )

    if address:
        target.customer_address = address[0].parent

    if contact:
        target.contact_person = contact[0].parent

    if getattr(source, 'sales_person', None):
        target.set('sales_team', [])
        target.append('sales_team', {
            "sales_person": getattr(source, 'sales_person', None),
            "allocated_percentage": "100",
            # "incentives":"150"
        })

        # dynamic.dynamic.elevana.api.get_customer_name


@frappe.whitelist(allow_guest=1)
def get_customer_name(*args, **kwargs):
    # get data
    data = False
    respone = Response()
    try:
        data = json.loads(frappe.request.data)
    except Exception as e:
        frappe.local.response['message'] = f"Error Accourd   {e}"
        frappe.local.response['http_status_code'] = 400

    if data:
        # check phone number
        phone_number = data.get("phone")
        user_extension = data.get("user_extension")
        if not phone_number:
            # frappe.local.response['message'] = "Customer name required"
            # frappe.local.response['http_status_code'] = 400
            respone.data = "error!"
            return

        if user_extension:
            user = frappe.db.get_value(
                "User", {"extension": user_extension}, 'name')
            if user:
                phone_call = frappe.new_doc("Phone Call")
                phone_call.posting_date = nowdate()
                phone_call.naming_series = 'PHN-CLL-.####'
                phone_call.user = user
                phone_call.phone_number = phone_number
                phone_call.save()
        sql = frappe.db.sql(f""" SELECT link_title FROM 
            `tabDynamic Link` WHERE parent in  (SELECT parent From `tabContact Phone` WHERE phone =  "{phone_number}" ) """, as_dict=1)

        if sql and len(sql) > 0:
            respone.data = str(sql[-1].get("link_title"))
        else:
            respone.data = str(phone_number)
        return respone


@frappe.whitelist()
def get_item_list(*args, **kwargs):
    price_list = frappe.db.get_single_value(
        "E Commerce Settings", "price_list")
    hub_items = frappe.get_list(
        "Item",
        filters={
            "publish_in_hub": 1,
            "disabled": 0
        },
        ignore_permissions=True,
        fields=[
            'item_code',
            'item_name',
            'item_group',
            'description',
            'item_code',
            'hub_warehouse as warehouse'
        ]
    )

    for item in hub_items:
        item.price = get_item_price(item.item_code, price_list) or 0
        item.stock_availability = "In Stock" if \
            frappe.db.get_value(
            "Bin",
            filters={
                        "item_code": item.item_code,
                        "warehouse": item.warehouse
                    },
            fieldname='actual_qty') or 0 \
            else "Out of Stock"

    frappe.response['items'] = hub_items





@frappe.whitelist()
def create_customer(*args, **kwargs):
    try :
        data = json.loads(frappe.request.data)
        # return data
        customer_name = data.get('customer_name')
        phone_no = data.get('phone_no')
        
        customer_group = frappe.db.get_single_value("E Commerce Settings", "default_customer_group")
        customer_territory = frappe.db.get_single_value("E Commerce Settings", "default_customer_territory")

        if not customer_name :
            frappe.response['status_code'] = 400
            frappe.response['message'] = _("{} is required").format(_('Customer Name'))
            return

        if not phone_no :
            frappe.response['status_code'] = 400
            frappe.response['message'] = _("{} is required").format(_('Phone No'))
            return

        if not customer_group :
            frappe.response['status_code'] = 400
            frappe.response['message'] = _("{} is required").format(_('Customer Group'))
            return

        if not customer_group :
            frappe.response['status_code'] = 400
            frappe.response['message'] = _("{} is required").format(_('Customer Territory'))
            return


        customer = frappe.new_doc('Customer')
        customer.customer_name = customer_name 
        customer.customer_group = customer_group
        customer.territory = customer_territory
        customer.phone_no = phone_no
        customer.woocommerce_customer_id = data.get("id")
        customer.save(ignore_permissions=True)
        if customer :
            create_customer_address(customer ,data)
            frappe.response['status_code'] = 200
            frappe.response['customer'] = customer
            return 
        else :
            error = frappe.new_doc("Error Log")
            error.method="create_customer"
            error.error = "Error Accour"
            error.save()
            frappe.response['status_code'] = 400
            frappe.response['message'] ="Can Not Save Customer"
            return 
        
    except Exception as e :
        error = frappe.new_doc("Error Log")
        error.method="create_customer"
        error.error = e
        error.save()
        frappe.response['status_code'] = 400
        frappe.response['message'] = e
        return 



def create_customer_address(customer, woocommerce_customer):
    billing_address = woocommerce_customer.get("billing")
    shipping_address = woocommerce_customer.get("shipping")
    
    if billing_address:
        country = "Egypt"
        # country = get_country_name(billing_address.get("country"))
        # if not frappe.db.exists("Country", country):
        #     country = "Switzerland"
        try :
            frappe.get_doc({
                "doctype": "Address",
                "woocommerce_address_id": "Billing",
                "address_title": customer.name,
                "address_type": "Billing",
                "address_line1": billing_address.get("address_1") or "Address 1",
                "address_line2": billing_address.get("address_2"),
                "city": billing_address.get("city") or "City",
                "state": billing_address.get("state"),
                "pincode": billing_address.get("postcode"),
                "country": country,
                "phone": billing_address.get("phone"),
                "email_id": billing_address.get("email"),
                "building_no" : billing_address.get("building_no"),
                "floor_no":billing_address.get("floor_no"),
                "apartment_no":billing_address.get("apartment_no"),
                "links": [{
                    "link_doctype": "Customer",
                    "link_name": customer.name
                }]
            }).insert()

        except Exception as e:
            error = frappe.new_doc("Error Log")
            error.method="create_customer_address"
            error.error = e
            error.save()
            # make_woocommerce_log(title=e, status="Error", method="create_customer_address", message=frappe.get_traceback(),
            #         request_data=woocommerce_customer, exception=True)

    if shipping_address:
        # country = get_country_name(shipping_address.get("country"))
        # if not frappe.db.exists("Country", country):
        country = "Egypt"
        try :
            frappe.get_doc({
                "doctype": "Address",
                "woocommerce_address_id": "Shipping",
                "address_title": customer.name,
                "address_type": "Shipping",
                "address_line1": shipping_address.get("address_1") or "Address 1",
                "address_line2": shipping_address.get("address_2"),
                "city": shipping_address.get("city") or "City",
                "state": shipping_address.get("state"),
                "pincode": shipping_address.get("postcode"),
                "country": country,
                "building_no" : shipping_address.get("building_no"),
                "floor_no":shipping_address.get("floor_no"),
                "apartment_no":shipping_address.get("apartment_no"),
                "phone": shipping_address.get("phone"),
                "email_id": shipping_address.get("email"),
                "links": [{
                    "link_doctype": "Customer",
                    "link_name": customer.name
                }]
            }).insert()
            
        except Exception as e:
            error = frappe.new_doc("Error Log")
            error.method="create_customer_address"
            error.error = e
            error.save()
            # make_woocommerce_log(title=e, status="Error", method="create_customer_address", message=frappe.get_traceback(),
            #     request_data=woocommerce_customer, exception=True)

# ToDO: email and phone into child table
def create_customer_contact(customer, woocommerce_customer):
    try :
        frappe.get_doc({
            "doctype": "Contact",
            "first_name": woocommerce_customer["billing"]["first_name"],
            "last_name": woocommerce_customer["billing"]["last_name"],
            "email_ids": [{
                "email_id": woocommerce_customer["billing"]["email"],
                "is_primary": 1
            }],
            "phone_nos": [{
                "phone": woocommerce_customer["billing"]["phone"],
                "is_primary_phone": 1
            }],
            "links": [{
                "link_doctype": "Customer",
                "link_name": customer.name
            }]
        }).insert()

    except Exception as e:
        #create Error
        error = frappe.new_doc("Error Log")
        error.method="create_customer_contact"
        error.error = e
        error.save()



def get_coupon_code(refal) :
    coupon = frappe.get_all("Coupon Code", filters=[["coupon_code", "=",refal]], fields=['name'])
    if coupon and len(coupon) > 0 :
        return coupon[0].get("name")
    return False

@frappe.whitelist()
def create_sales_order(*args, **kwargs):
    try :
        # return json.loads(frappe.request.data)
        data = json.loads(frappe.request.data)
        id = data.get("customer_id")
        customer = frappe.get_all("Customer", filters=[["woocommerce_customer_id", "=", id]], fields=['name'])
        # customer_name = data.get('customer_id')
        items = data.get('items')
        
        # return frappe.get_doc("Customer" , customer_name)
        # return frappe.db.exists("Customer" , "pewter")
        # if frappe.db.exists("Customer" , customer_name) :
        #     customer = frappe.get_doc("Customer" , customer_name)

        company = frappe.db.get_single_value("E Commerce Settings", "company")
        price_list = frappe.db.get_single_value("E Commerce Settings", "price_list")


        if not customer :
            frappe.response['status_code'] = 400
            frappe.response['message'] = _("{} is required").format(_('Customer'))
            return

        if not customer :
            frappe.response['status_code'] = 400
            frappe.response['message'] = _("{} is invalid").format(_('Customer'))
            return
        
        # print (frappe.request.post)
        print (type(items))
        if type(items) is str :
            items = json.loads(str(items))
        
        print (type(items))
        # items = json.loads(str(items))
        # return
        print(customer )
        if not items :
            frappe.response['status_code'] = 400
            frappe.response['message'] = _("{} is required").format(_('Items'))
            return


        
        
        order = frappe.new_doc("Sales Order")
        
        order.customer = customer[0].get("name")
        order.company = company
        order.currency = get_company_currency(company)
        order.price_list = price_list
        order.order_type = "Sales"
        order.delivery_date = nowdate()
        # order.woocommerce_order_id = data.get("order_id")
        order.conversion_rate = 1
        order.cost_center = get_default_cost_center(company)
        
        warehouse = None
        for item in items or []:
            #it=frappe._dict(it)
           
            item_code = item.get("item_code")
            print("item Code" , item_code)
            if frappe.db.exists("Item" , item_code) :
                item_doc = frappe.get_doc("Item" , item_code)

            if not item_doc :
                frappe.response['status_code'] = 400
                frappe.response['message'] = _("{} is invalid").format(_('Item'))
                return
            
            row = order.append("items",{})
            row.item_code = item_code
            row.warehoue = item_doc.hub_warehouse
            warehouse = item_doc.hub_warehouse
            row.qty= item.get ("qty")
            row.price_list_rate= item.get("rate")
        order.set_warehouse = warehouse
        order.save()
        if data.get("coupon_code" ) :
            coupon = get_coupon_code(data.get("coupon_code" )) 
            if coupon :
                order.coupon_code = coupon
        order.save()
        frappe.response['order'] = order
        return 
    except Exception as e :
        error = frappe.new_doc("Error Log")
        error.method="create_order"
        error.error = e
        error.save()
        frappe.response['status_code'] = 400
        frappe.response['message'] = _("{} ").format(_(e))
        return




@frappe.whitelist(allow_guest=True)
def get_couponcode_data(*args, **kwargs):
    """
    Get Sales Patener Data And Coupon Code 
    
    
    """
    data = frappe.db.sql(""" 
    SELECT a.referral_code as code , a.name as marketer ,b.pricing_rule ,
    c.rate_or_discount,c.discount_percentage , c.discount_amount ,c.rate
      FROM `tabSales Partner` a  
    INNER JOIN `tabCoupon Code` b 
    INNER JOIN `tabPricing Rule` c
    ON a.referral_code = b.coupon_code AND c.name=b.pricing_rule


    """,as_dict=1)
    return {"data":data }








#dynamic.elevana.api
# create coupon code 
# 
"""
{
"code" : " " , 
"type" : "fixed_cart" , 
"amount" : " " , 
"usage_limit":"" ,
"expiry_date":"",
"minimum_amount":"",
}
update 
{
"coupon_id" :""
"code" : " " , 
"type" : "fixed_cart" , 
"amount" : " " , 
"usage_limit":"" ,
"expiry_date":"",
"minimum_amount":"",
}
from dynamic.elevana.api import create_coupon_code

create_coupon_code('hnuim' ,False)

"""
def create_coupon_code(code , update=False,*args ,**kwargs ) :
    #get code required data 
    data = frappe.get_doc("Coupon Code" , code)
    rule = False
    if data.pricing_rule : 
         rule = frappe.get_doc("Pricing Rule" ,data.pricing_rule )
    pay_load = {
        "code": data.name ,
        "type" : "fixed_cart" ,
        "amount" : float(rule.discount_amount or 0) if rule else 0 ,
        "usage_limit":data.maximum_use , 
        "expiry_date" : data.valid_upto , 
        "minimum_amount":1,

    }
    if update  :
        pay_load["coupon_id"] = data.wooid 

    #connsction settings 
    dt = frappe.db.sql(""" SELECT name ,post , put  FROM `tabCoupon Code Setting` WHERE is_active  ="1" """ ,as_dict =1)
    if dt and len(dt) > 0 :
       url =dt[0].get("put")  if update else  dt[0].get("post") 
       print(url)
       res = requests.get(f"{url}" ,params=pay_load)

       if res.status_code != 200 :
           #create Error 
           print("Error" ,res.text)
           error = frappe.new_doc("Error Log")
           error.method="create_Copon Code Error"
           error.error = res.text
           error.save()
           pass
           #frappe.new_doc("Error Log")
       if not update :
           d=  res.json()
           print("success" , d )
           data.wooid = d.get("data").get("id")
           data.save()
           frappe.db.commit()
           error = frappe.new_doc("Error Log")
           error.method="create Copon Code Success"
           error.error = res.text
           error.save()
       if update :
           error = frappe.new_doc("Error Log")
           error.method="update  Copon Code Success"
           error.error = res.text
           error.save()
           
          
       
    else :
        frappe.throw("No WooCommerce data Found !")

def create_new_code(doc, *args ,**kwargs) :
    DOMAINS = frappe.get_active_domains()
    if  'Elevana' in DOMAINS and not doc.is_new() : 
        #
        # check price Rule 
        if not doc.pricing_rule :
            frappe.throw("Please set price Rule")

        if not not doc.valid_upto :
            doc.valid_upto = "2999-01-01"
        if not doc.maximum_use :
            doc.maximum_use = 10000
        #post to woocommerce 
        if not doc.wooid :
            create_coupon_code(doc.name , update=False)
        # frappe.throw("New Doc")
        if doc.wooid :
            create_coupon_code(doc.name , update=True)