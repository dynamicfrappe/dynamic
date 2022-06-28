from __future__ import unicode_literals
from sys import flags

import frappe
from frappe import _
from frappe.utils.data import flt
from dynamic.api import create_reservation_validate
DOMAINS = frappe.get_active_domains()

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_item_query(doctype, txt, searchfield, start, page_len, filters):
    comparison = filters.get("comparison") or ''
    search_txt = "%%%s%%" % txt

    return frappe.db.sql(f"""select item.name , item.item_name
                    from tabItem item
                    inner join `tabComparison Item` child
                        on  child.clearance_item = item.name
                    where child.parent = '{comparison}'
                    and (item.name like '{search_txt}' or item.item_name like '{search_txt}' )""")


@frappe.whitelist()
def on_submit(self,fun=''):
    if getattr(self,"against_comparison",False) :
        comparison = frappe.get_doc("Comparison",self.comparison)
        for item in getattr(self,"items",[]):
            comparison_item = [ x for x in getattr(comparison,"item",[]) if x.clearance_item == item.comparison_item ]
            if len(comparison_item) > 0:
                    comparison_item = comparison_item [0]
                    if not comparison_item.allow_material_over_price :
                        # comparison_item.total_price
                        result = frappe.db.sql(f"""
                        select SUM(child.basic_amount) as total_price from `tabStock Entry` se
                        inner join `tabStock Entry Detail` child on child.parent = se.name
                        where se.docstatus = 1 and se.against_comparison = 1 
                        and child.comparison_item = '{item.comparison_item}'
                        """ , as_dict=1)
                        if result :
                            total_price = result[0].total_price or 0
                            if flt(total_price + item.basic_amount) >  flt(comparison_item.price) : 
                                frappe.throw(_("Can't Allow to Submit Material Request \nItem {} Price {} is more than Comparison {} item Price {}").format(
                                    item.item_name , 
                                    flt(total_price + item.basic_amount),
                                    self.comparison ,
                                    comparison_item.total_price
                                ))



@frappe.whitelist()
def update_project_cost(self,*args , **kwargs):
    
    
    if 'Contracting' in DOMAINS :
   
        if self.comparison :
            comparison = frappe.get_doc("Comparison" , self.comparison )
            self.estimated_cost = float(comparison.total_cost_amount or 0)
        if self.project :
            all_projects  = frappe.db.sql(
                """ SELECT SUM(estimated_cost) as cost FROM `tabSales Order` WHERE project = '%s' """%self.project ,as_dict=True
            )   
            project = frappe.get_doc("Project" , self.project )
            project.estimated_costing = float(all_projects[0].get("cost") or 0)
            project.save()

    # if "Terra" in DOMAINS:
    #     ## call method from api 
    #     create_reservation_validate(self,*args , **kwargs)
