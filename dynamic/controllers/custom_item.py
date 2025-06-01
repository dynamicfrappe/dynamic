
import frappe 
import json
from frappe.model.naming import make_autoname,set_name_by_naming_series,determine_consecutive_week_number,NAMING_SERIES_PART_TYPES
import datetime
import re
from frappe.utils import flt
from six import string_types
import frappe
from frappe import _
from frappe.model import log_types
from frappe.utils import cint, cstr, now_datetime
from frappe.utils import getdate, nowdate


@frappe.whitelist()
def show_next_name(doc):
    # pass
    item_naming_by = frappe.db.get_single_value('Stock Settings','item_naming_by')
    nex_name = ''
    if item_naming_by == "Naming Series":
        doc = json.loads(doc)
        nex_name = make_autoname(doc.get('naming_series'), "", doc)
    return {'new_name':nex_name}
    

def make_autoname(key="", doctype="", doc=""):
    """
        Creates an autoname from the given key:

         **Autoname rules:**

                  * The key is separated by '.'
                  * '####' represents a series. The string before this part becomes the prefix:
                        Example: ABC.#### creates a series ABC0001, ABC0002 etc
                  * 'MM' represents the current month
                  * 'YY' and 'YYYY' represent the current year


    *Example:*

                  * DE/./.YY./.MM./.##### will create a series like
                    DE/09/01/0001 where 09 is the year, 01 is the month and 0001 is the series
    """
    if key == "hash":
        return frappe.generate_hash(doctype, 10)

    if "#" not in key:
        key = key + ".#####"
    elif "." not in key:
        error_message = _("Invalid naming series (. missing)")
        if doctype:
            error_message = _("Invalid naming series (. missing) for {0}").format(doctype)

        frappe.throw(error_message)

    parts = key.split(".")
    n = parse_naming_series(parts, doctype, doc)
    return n

def parse_naming_series(parts, doctype="", doc=""):
    n = ""
    if isinstance(parts, str):
        parts = parts.split(".")
    series_set = False
    today = now_datetime()
    for e in parts:
        if not e:
            continue

        part = ""
        if e.startswith("#"):
            if not series_set:
                digits = len(e)
                part = getseries(n, digits)
                series_set = True
        elif e == "YY":
            part = today.strftime("%y")
        elif e == "MM":
            part = today.strftime("%m")
        elif e == "DD":
            part = today.strftime("%d")
        elif e == "YYYY":
            part = today.strftime("%Y")
        elif e == "WW":
            part = determine_consecutive_week_number(today)
        elif e == "timestamp":
            part = str(today)
        elif e == "FY":
            part = frappe.defaults.get_user_default("fiscal_year")
        elif e.startswith("{") and doc:
            e = e.replace("{", "").replace("}", "")
            part = doc.get(e)
        elif doc and doc.get(e):
            part = doc.get(e)
        else:
            part = e

        if isinstance(part, str):
            n += part
        elif isinstance(part, NAMING_SERIES_PART_TYPES):
            n += cstr(part).strip()
    
    return n

def getseries(key, digits):
    # series created ?
    sql ="SELECT `current` FROM `tabSeries` WHERE `name`='%s' "%key

    current = frappe.db.sql(sql)
    
    if current and current[0][0] is not None:
        current = current[0][0] +1
    else:
        # no, create it
        current = 1
    return ("%0" + str(digits) + "d") % current


def update_payment_term_status():
    if "captain" not in frappe.get_active_domains():
        return
    today = getdate(nowdate()) 
    terms = frappe.get_all("Payment Term", fields=["name", "disable_on"])
    for term in terms:
        disable_on = getdate(term.disable_on) if term.disable_on else None
        if disable_on and disable_on <= today:
            is_usable = 0
        else:
            is_usable = 1
        frappe.db.set_value("Payment Term", term.name, "is_usable", is_usable)
        print(f"Updated {term.name} to is_usable = {is_usable}")
    frappe.db.commit()
    
    

def before_save(doc, method):
    if "captain" not in frappe.get_active_domains():
        return
    total_amount = sum(flt(i.amount) for i in doc.items)
    maintenance_percent = flt(doc.maintenance_payment_percent)
    maintenance_payment = flt(doc.maintenance_payment)
    # if maintenance_percent > 0 and maintenance_payment > 0:
    #     frappe.throw("You can use either Maintenance Payment or Maintenance Payment Percent, not both.")
    if maintenance_percent:
        doc.maintenance_payment = total_amount * maintenance_percent / 100
    elif maintenance_payment:
        doc.maintenance_payment_percent = (maintenance_payment / total_amount) * 100
    if doc.maintenance_payment and not doc.warehouse_amount:
        doc.grand_total += (doc.maintenance_payment)
    elif doc.maintenance_payment and doc.warehouse_amount:
        doc.grand_total += (doc.maintenance_payment +doc.warehouse_amount)




def update_total_amount_in_item(self, method):
    if "Real State" not in frappe.get_active_domains():
        return
    item_code = self.item_code
    if not frappe.db.exists("Item", item_code):
        return
    current_price = frappe.db.get_value("Item Price", {"item_code": item_code, "selling": 1}, "price_list_rate")
    if current_price != self.total_price:
        item_price = frappe.get_all(
            "Item Price",
            fields=["name"],
            filters={"item_code": item_code, "selling": 1}
        )
        if item_price:
            frappe.db.set_value(
                "Item Price",
                item_price[0].name,
                "price_list_rate",
                self.total_price
            )
        else:
                frappe.get_doc({
                    "doctype": "Item Price",
                    "item_code": item_code,
                    "price_list": "Standard Selling",  
                    "price_list_rate": self.total_price,
                    "selling": 1
                }).insert()

def update_th_staues_of_the_items():
    from datetime import datetime
    if "Real State" not in frappe.get_active_domains():
        return
    today = datetime.today().date()
    items = frappe.get_all(
        "Item",
        fields=["name", "vaild_to", "disabled", "status"],
        filters={"vaild_to": today}
    )
    for item in items:
        item_doc = frappe.get_doc("Item", item.name)
        item_doc.disabled = 1
        item_doc.status = "On hold"
        item_doc.save()
    frappe.db.commit()
    items = frappe.get_all(
        "Item",
        fields=["name", "vaild_to", "disabled", "status"],
        filters={"vaild_to": [">", today]}
    )
    for item in items:
        item_doc = frappe.get_doc("Item", item.name)
        item_doc.disabled = 0
        item_doc.status = "Available To Sell"
        item_doc.save()
    frappe.db.commit()


from frappe.utils import get_datetime, now_datetime, to_timedelta
from datetime import timedelta
def delete_ended_qutation():
    if "Real State" not in frappe.get_active_domains():
        return
    settings = frappe.get_single("Real Estate Sittings")
    duration_str = settings.end_date 
    try:
        end_duration = to_timedelta(duration_str)
    except Exception as e:
        frappe.log_error(f"Invalid duration in end_date: {duration_str}", "Quotation Auto Cancel Error")
        return
    quotations = frappe.get_list(
        "Quotation",
        filters={"status": "Open"},
        fields=["name", "transaction_date", "creation"]
    )
    for q in quotations:
        transaction_date = get_datetime(q.transaction_date)
        expiry_datetime = transaction_date + end_duration
        if now_datetime() > expiry_datetime:
            doc = frappe.get_doc("Quotation", q.name)
            if doc.docstatus == 1:
                doc.cancel()
                print(f"Cancelled Quotation {q.name} at {now_datetime()} (expired after {end_duration})")
    print(quotations)
    print("End Days from settings:", duration_str)

def before_save_total_grand(doc, method):
    if "Real State" not in frappe.get_active_domains():
        return
    if doc.grand_total and hasattr(doc, "payment_schedule"):
        for row in doc.payment_schedule:
            row.payment_amount = (doc.grand_total * row.invoice_portion)/100
