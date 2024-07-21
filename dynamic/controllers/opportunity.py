import frappe 
from frappe.utils import today
Domains = frappe.get_active_domains()

def close_ended_opportunity(*args , **kwargs) :

    if "Terra"  in Domains :
        day = today()
        sales_order_op = frappe.db.sql(""" SELECT DISTINCT opportunity FROM `tabSales Order` """)

        show_data = frappe.db.sql(f""" SELECT name FROM `tabOpportunity` WHERE name in (
        SELECT name FROM `tabOpportunity` where status ="Open" 
        and date(expected_closing) < date('{day}') )""" ,as_dict=1)

        print(show_data)
        update_sql = frappe.db.sql(f""" 
        UPDATE tabOpportunity set status= "Open"  where name in (
        SELECT name FROM `tabOpportunity` where status = "Closed"
       ) 
        and name not in (SELECT DISTINCT opportunity FROM `tabSales Order`)  ; 
        
        """)
        frappe.db.commit()