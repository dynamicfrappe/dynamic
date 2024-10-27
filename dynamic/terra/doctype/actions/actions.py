# Copyright (c) 2022, Dynamic and contributors
# For license information, please see license.txt
import json
import frappe
from frappe.model.document import Document

class Actions(Document):
	pass
@frappe.whitelist()
def get_events(start, end, filters=None):
    """Returns events for Gantt / Calendar view rendering.

    :param start: Start date-time.
    :param end: End date-time.
    :param filters: Filters (JSON).
    """
    from erpnext.controllers.queries import get_match_cond
    from frappe.desk.calendar import get_event_conditions

    # Load filters if provided
    filters = json.loads(filters) if filters else {}
    conditions = get_event_conditions("Actions", filters)

    # Fetch events based on start and end dates and any additional conditions
    data = frappe.db.sql(
        """
        SELECT
            `tabActions`.name AS name,
            `tabActions`.`from1` AS start,
            `tabActions`.`to` AS end
        FROM
            `tabActions`
        WHERE
            (`tabActions`.`from1` BETWEEN %(start)s AND %(end)s)
            {conditions}
        """.format(conditions=conditions),
        {"start": start, "end": end},
        as_dict=True,
        update={"allDay": 0}
    )
    return data

