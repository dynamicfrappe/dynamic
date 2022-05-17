import frappe
from frappe import _
from datetime import datetime ,date
DOMAINS = frappe.get_active_domains()

"""  
Fiscal Year Is The Committion Function Main Key 
Under The  Fiscal Year Sales Invocie Month will Be The Count Method 

"""

def validate_fiscal_year(year):
    """   this function Check if the year is Disabled  and If company Belong to The year  """

    fiscal_year = frappe.get_doc("Fiscal Year" , year)
    if fiscal_year.disabled :
        frappe.throw("You Can Not Caculate Commetion To  Disabled Year   ")
        return 0
    
    company =frappe.defaults.get_user_default("Company")
    if fiscal_year.companies :
        company_list = [co.company for co in fiscal_year.companies ]
        if  company not in company_list :
            frappe.throw(f""" Commetion  Table dos Not Belong To Company {company}""")
            return 0
        
    return True



def validate_sales_person(name) :
    """  Get All Sales Person From The Invoice """
   
    sales_person = frappe.get_doc("Sales Person" , name)
    if sales_person.is_group == 1 :
        pass
        return 0 
    if sales_person.enabled == 0 :
        frappe.throw(f""" Sales Person {name} Is Not Active \n
         Please Enable Sales Person Before Complete Sales Invocie """)
    """Get Person Template  """
    if not sales_person.targets :
        return 0
    
    for target in sales_person.targets :
        #1 - validate Fiscal Year 
        fiscal_year = target.fiscal_year
        if not fiscal_year :
            frappe.throw(""" Please Set fiscal year To Sales Person Target Table """)
        validate_fiscal_year(fiscal_year)
        #validate Target  amount , Qty And get Mothly Target 
        # vaildate targey qty
        template = frappe.get_doc("Commission Template" ,target.commission_template )
        if target.target_qty > 0  and target.target_amount > 0 :
            frappe.throw(""" Please Set arget Qty  or  Target Amount to 0 value in Target Table """)
        if target.target_qty == 0  and target.target_amount == 0 :
            frappe.throw(""" Please Set arget Qty  or  Target Amount to  value in Target Table """)
        #validate template with target qty 
        if target.target_qty > 0  and target.commission_template:
            if template.base_on == "Amount" :
                      frappe.throw(""" Commission Base On Qty Please Select   Commission Template Based On Qty """)
           
        if target.target_amount > 0  and target.commission_template:
            if template.base_on == "Qty" :
                      frappe.throw(""" Commission Base On Qty Please Select   Commission Template Based On Qty """)
        #caclulate Mothly Invoice For sales Man 
       
        #test Area Not Used
        caculation_sql =    f""" SELECT `tabSales Invoice`.posting_date as date , 
                                `tabSales Invoice Item`.amount as amount
                                FROM 
                                `tabSales Invoice` INNER JOIN 
                                `tabSales Invoice Item`
                                ON `tabSales Invoice`.name = `tabSales Invoice Item`.parent
                                WHERE `tabSales Invoice`.name in 
                                (SELECT parent FROM `tabSales Team` WHERE sales_person = '{name}')
                                AND `tabSales Invoice`.docstatus = 1
                            """
        # data = frappe.db.sql(caculation_sql ,as_dict=1)
        # frappe.throw(str(data))
"""  this method Will Run only if Moyate in Active Domain """
def filetr_item_base_on_template(items , person , pdate) :
    #caculate item percent 
    # frappe.throw(str(items))
    date_list = str(pdate).split('-')
    year_name = date_list[0]
    month_name = date_list[1]
    item_group_amount = []
    sales_person = frappe.get_doc("Sales Person" ,person)
    commetion_item_group = [target.item_group for target in sales_person.targets]
    invocie_item_groups = [item.get("item_group") for item in items ]
    for group in invocie_item_groups :
        if group not in invocie_item_groups :
            invocie_item_groups.pop(group)
    # frappe.throw("str" +str(invocie_item_groups) + "Str" +str(commetion_item_group) ) 

    """  
    Caculate Item Group total Sales For Sales Person 

    """
    #remove Duplicated FROM  invocie_item_groups
    invocie_item_groups = set(invocie_item_groups)
    item_group_tuple = list(invocie_item_groups)
   
    for item_group in item_group_tuple :
        local_sales = 0
        local_qty = 0 
        for item in items :
            if item.get("item_group") == item_group :
                local_sales = local_sales + float(item.get("amount"))
                local_qty = local_qty + float(item.get("qty"))
        start_date = f"""{year_name}-{month_name}-01"""
        end_date = f"""{year_name}-{month_name}-31"""
        caculation_sql =    f"""   SELECT 
                                    SUM(`tabSales Invoice Item`.amount) as amount ,
                                    SUM(`tabSales Invoice Item`.qty) as qty
                                    FROM 
                                    `tabSales Invoice` INNER JOIN 
                                    `tabSales Invoice Item`
                                    ON `tabSales Invoice`.name = `tabSales Invoice Item`.parent
                                    WHERE `tabSales Invoice`.name in 
                                    (SELECT parent FROM `tabSales Team` WHERE sales_person = '{person}')
                                    AND `tabSales Invoice`.docstatus = 1 and
                                    `tabSales Invoice Item`.item_group = '{item_group}' and 
                                    `tabSales Invoice`.posting_date between '{start_date }' and '{end_date}' 
                                """
       
        old_sales_amount = 0 
        old_sales_qty = 0
        sum_amount = frappe.db.sql(caculation_sql ,as_dict=1)
        if sum_amount and len(sum_amount) > 0 :
            old_sales_amount = sum_amount[0].get("amount")   
            old_sales_qty =    sum_amount[0].get("qty")
        total_monthly_sales = float(old_sales_amount or 0) +float(local_sales or 0)
        total_monthly_qty = float(old_sales_qty or 0 ) + float(local_qty or 0)
        # find Commission in Commission Template
        template_sql = f""" SELECT commission_template FROM `tabTarget Detail`  WHERE    
        fiscal_year = '{year_name}' and parent = '{person}' and item_group = '{item_group}'

            """
        commition_amount = 0
        commition_rate = 0 
        grant_commition = 0 
        template = frappe.db.sql(template_sql ,as_dict =1)
        if template and len(template) > 0 :
            local_template = frappe.get_doc("Commission Template" , template[0].get("commission_template"))
            if local_template.base_on ==  "Amount" :
                for in_amount in local_template.templat  :
                    if float(total_monthly_sales) > float(in_amount.amount_from or  0)  and local_template.base_on ==  "Amount":
                        commition_amount  = float(in_amount.commission_amount or 0 )
                        commition_rate    = float(in_amount.commission_rate or 0 )
            if local_template.base_on ==  "Qty" : 
                for in_amount in local_template.templat  :
                    if float(total_monthly_qty) > float(in_amount.amount_from or  0) :
                        commition_amount  = float(in_amount.commission_amount or 0 )
                        commition_rate    = float(in_amount.commission_rate or 0 )
        grant_commition = commition_amount
        if  commition_rate  > 0 :
            grant_commition = float(total_monthly_sales) * (float(commition_rate or 0 ) /100)

        return grant_commition
        pass
    return 0 
@frappe.whitelist()
def validate_sales_invocie_to_moyate(self):
    """  
    Calculate the Commetion For Sales Person Base on Commission Template
    Disabled Sales Person throw Error
    if Sales Person is Group function will not work with no Errors   
    How To Use  : - 
                1 - Create Commission Table in Commission Table List
                2 - In Sales Person Add The Link of The Commition table To the Targets Table 
                3 - 
    """
    if self.sales_team :
        # frappe.throw(" Sales Team Found")
        for person in self.sales_team :
            sales_person = validate_sales_person(person.sales_person)
            #caculate Commition Base On total Amount Before Tax 
            cal_precent = float(person.allocated_percentage) /100
            #data = allocated_percentage ,  sales_person , Items ,  date
            filtersitems = filetr_item_base_on_template([{  "item_code"  :item.item_code ,
                                                            "item_group" :item.item_group ,
                                                            "amount"     :float(item.base_amount) *cal_precent  ,
                                                            "qty" :item.qty} 
                                                             for item in  self.items] , 
                                                             person.sales_person ,
                                                             self.posting_date)
            person.incentives = filtersitems
    pass


