import frappe
from frappe.utils import date_diff , now
DOMAINS = frappe.get_active_domains()


def check_data_remaining():
    if 'Logistics' in DOMAINS: 
        containers = frappe.db.get_list(
                    "PO Container",
                    filters={
                        "status": "Ordered",
                    },
                    pluck = "name")
        print(containers)
        for container in containers :
            container = frappe.get_doc("PO Container" , container)
            if not container.remaining_date :
                differance = date_diff( container.arrived_date ,now() )
                container.remaining_date = f'{differance}' + " days"
                if differance < 0 :
                    container.status = "Overdue"
                container.save()

@frappe.whitelist()
def calculate_payments(quotation):
    if 'Logistics' in DOMAINS:
        sql = f'''
            SELECT SUM(PE.paid_amount) AS sum 
            FROM 
                `tabPayment Entry` PE
            INNER JOIN 
                `tabPayment Entry Reference` PER
            ON
                PE.name = PER.parent
            WHERE
                PER.reference_name = '{quotation}'
                '''
        
        data = frappe.db.sql(sql , as_dict = 1)
        total_payments = data[0]["sum"]
        return total_payments