# Copyright (c) 2022, Dynamic and contributors
# For license information, please see license.txt
import json
import frappe
from frappe.model.document import Document

class Actions(Document):
    pass
@frappe.whitelist()
def get_events(start, end, filters=None):
    from erpnext.controllers.queries import get_match_cond
    from frappe.desk.calendar import get_event_conditions

    filters = json.loads(filters) if filters else {}
    conditions = get_event_conditions("Actions", filters)

    data = frappe.db.sql(
        """
        SELECT
            `tabActions`.name AS name,
            `tabActions`.`start` AS start,
            `tabActions`.`end` AS end
        FROM
            `tabActions`
        WHERE
            (`tabActions`.`start` BETWEEN %(start)s AND %(end)s)
            {conditions}
        """.format(conditions=conditions),
        {"start": start, "end": end},
        as_dict=True,
        update={"allDay": 0}
    )
    
    return data

