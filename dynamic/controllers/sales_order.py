



import frappe
from frappe import _
from frappe.utils import date_diff , now , add_days ,getdate
from dynamic.qaswaa.controllers.sales_order_api import validate_item_qty_reserved

Domains=frappe.get_active_domains()

def validate_sales_order(self , event):
    if "Qaswaa" in Domains :
        validate_item_qty_reserved(self,event)
    if 'Logistics' in Domains :
        validate_qotation(self)
        validate_sales_order_items(self)
        if not self.update_validation_date :

            set_vaild_until_date(self)
        # validate_so(self)
        validate_advances_item(self)

def validate_so(self):
    grand_total = self.grand_total 
    sql1 = f'''
        SELECT 
            SO.name 
        FROM
            `tabSales Order` SO
        WHERE 
            DATE(SO.valid_until) < DATE('{getdate(now())}')
            and
            SO.grand_total <
        '''
    data = frappe.db.sql(sql1, as_dict=1)
    if data :
        for entry in data :   
            sql1 = f'''
                SELECT 
                    SI.name 
                FROM
                    `tabSales Invoice Item` SI
                WHERE 
                    SI.sales_order = '{entry["name"]}'
                '''
            sales_invoice_item = frappe.db.sql(sql1 , as_dict = 1)
            if sales_invoice_item :
                pass
                # frappe.throw(str(sales_invoice_item))
        
def validate_advances_item(self):
    sum = 0
    if self.advances :
        for item in self.advances :
            sum += item.allocated_amount
        self.advance_paid = sum 
        self.outstanding_amount = self.grand_total - self.advance_paid
        for payment in self.payment_schedule :
            payment.payment_amount = (payment.invoice_portion /100 * self.outstanding_amount)



def submit_sales_order(self , event) :
    if 'Logistics' in Domains :
        set_serial_number_customer(self)

def validate_qotation(self):
    diable_order_without_quotation = frappe.db.get_single_value("Selling Settings", "diable_order_without_quotation")
    if diable_order_without_quotation == 0 :
        for d in self.get("items"):
            if d.prevdoc_docname:
                validate_total_payment_of_quotation(self , d)
                
    elif diable_order_without_quotation == 1 :
        for d in self.get("items"):
            if not d.prevdoc_docname:
                frappe.throw(_("Item {} must be from quotation").format(d.item_code))
            validate_total_payment_of_quotation(self , d)


def validate_total_payment_of_quotation(self , d):
    quotation = f'''
                SELECT 
                    Q.grand_total
                FROM 
                    `tabQuotation` Q
                WHERE
                    Q.name = '{d.prevdoc_docname}'
                    AND 
                    Q.docstatus = 1
                '''
    grand_total = frappe.db.sql(quotation , as_dict = 1 )
    grand_total_quotation = grand_total[0]["grand_total"]
    allowed_amount = (grand_total_quotation * 15) / 100 
    if grand_total_quotation :             
        sql = f'''
                SELECT 
                    SUM(PE.paid_amount) as sum
                FROM 
                    `tabPayment Entry` PE
                INNER JOIN 
                    `tabPayment Entry Reference` PER
                ON 
                    PE.name = PER.parent 
                WHERE 
                    PER.reference_name = '{d.prevdoc_docname}' 
                    AND 
                    PE.docstatus = 1
            '''
        data = frappe.db.sql(sql , as_dict = 1)
        total_paid_amout = data[0]["sum"]
        if not total_paid_amout :
            frappe.throw("30% of quotion must be paid")
        if not (total_paid_amout >= allowed_amount):
            frappe.throw("Total paid amount must be bigger than or eqal 30% of quotation total")


def validate_sales_order_items(self):
    items = []
    for item in self.items:
        if item.item_code in items :
            frappe.throw(_(f" Please Dont duplicat Item {item.item_code } in many lines !"))
        if not item.warehouse : 
            frappe.throw(_(f"Please Set item {item.item_code}"))
        sql = f'''
                SELECT 
                    B.name 
                    ,     (B.actual_qty +  B.ordered_qty - B.reserved_qty) as qty
                FROM
                    `tabBin` B
                WHERE 
                    B.item_code = '{item.item_code}' AND B.warehouse = '{item.warehouse}' 

                '''
        data = frappe.db.sql(sql , as_dict = 1)
        if not data :
            frappe.throw(_("Item <b>{0}</b> don't has actual qty in bin").format(item.item_name))
        if data and len(data) > 0 :
            actual_qty =  data[0].get("qty")
            if float(actual_qty  or 0 ) < float(item.qty) :
                frappe.throw(_(f"Available  item {item.item_code} qty for sales is {actual_qty} and you try to order {item.qty}"))
        items.append(item.item_code)
def set_serial_number_customer(self):
    if self.customer :
        for item in self.items:
            if len(item.serial_number) > 0  :
                serial_doc = frappe.get_doc("Serial No" , item.serial_number)
                serial_doc.customer = self.customer
                serial_doc.save()

def set_vaild_until_date(self):
    self.valid_until = add_days(now() , 7)
