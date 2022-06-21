import frappe
from frappe import _
DOMAINS = frappe.get_active_domains()
def validate_sales_invoice(doc,*args,**kwargs):
    if 'Gebco' in DOMAINS:
        if doc.maintenance_template:
            m_temp = frappe.get_doc("Maintenance Template",doc.maintenance_template)
            m_temp.sales_invoice = doc.name
            m_temp.save()
        if doc.maintenance_contract:
            contract_doc = frappe.get_doc("Maintenance Contract",doc.maintenance_contract)
            contract_doc.sales_invoice = doc.name
            contract_doc.save()
def validate_delivery_note(doc,*args,**kwargs):
    if 'Gebco' in DOMAINS:
        if doc.maintenance_template:
            m_temp = frappe.get_doc("Maintenance Template",doc.maintenance_template)
            m_temp.delivery_note = doc.name
            m_temp.save()

def validate_purchase_recipt(doc,*args,**kwargs):
    if 'Gebco' in DOMAINS:
        for item in doc.items:
            serial_list = str(item.serial_no).splitlines()
            if item.serial_no:
                if item.serial2:
                    s2_list = item.serial2.splitlines()
                    if len(serial_list) == len(s2_list):
                        for i in range(0,len(serial_list)):
                            sql= """select name from `tabSerial No` where serial2='%s'"""%s2_list[i]
                            res = frappe.db.sql(sql,as_dict=1)
                            if len(res) > 0:
                                frappe.throw(_(f"Serial No {s2_list[i]} Already Exist"))
                            serial_doc = frappe.get_doc("Serial No",serial_list[i])
                            serial_doc.serial2 = s2_list[i]
                            serial_doc.save()
                    else:
                        frappe.throw(_("Serial No list Doest Not Equal Serial2"))