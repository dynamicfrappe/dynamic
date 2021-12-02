from __future__ import unicode_literals

import frappe
from frappe import _



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