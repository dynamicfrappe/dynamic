import frappe
from frappe import _
from frappe.utils import (
    getdate,
    add_days,
    add_months,
    cint,
    flt,
    formatdate,
    get_first_day,
)
from dynamic.future.financial_statements import validate_dates


def get_period_list(filters):
    """
    Generates a list of periods (monthly) based on the given start and end dates.
    """
    period_start_date = filters.get("period_start_date")
    period_end_date = filters.get("period_end_date")

    validate_dates(period_start_date, period_end_date)

    start_date = getdate(period_start_date)
    end_date = getdate(period_end_date)

    months_to_add = 1
    period_list = []

    while start_date <= end_date:
        period = frappe._dict({"from_date": start_date})
        to_date = add_months(get_first_day(start_date), months_to_add)
        to_date = add_days(to_date, -1)

        # Ensure the period does not exceed the end date
        period["to_date"] = min(to_date, end_date)
        period["key"] = period["to_date"].strftime("%b_%Y").lower().replace(" ", "_").replace("-", "_")
        period["label"] = formatdate(period["to_date"], "MMM YYYY")

        period_list.append(period)

        start_date = add_months(start_date, months_to_add)

    return period_list


def get_data(filters=None):
    """
    Fetches data for the report based on the provided filters.
    """
    data = []
    conditions = []

    if filters.get("item"):
        conditions.append(f"a.item_code = '{filters.get('item')}'")
    if filters.get("supplier"):
        conditions.append(f"b.supplier = '{filters.get('supplier')}'")
    if filters.get("cost_center"):
        cost_centers = [{"cost_center": filters.get("cost_center")}]
        conditions.append(f"b.cost_center = '{filters.get('cost_center')}'")
    if filters.get("warehouse"):
        conditions.append(f"b.set_warehouse = '{filters.get('warehouse')}'")
    if filters.get("item_group"):
        conditions.append(f"a.item_group = '{filters.get('item_group')}'")

    # Build conditions string
    where_clause = " AND ".join(conditions) if conditions else "1=1"

    # Retrieve cost centers
    cost_centers = frappe.db.sql(
        """
        SELECT DISTINCT a.cost_center AS cost_center
        FROM `tabPurchase Invoice` a
        WHERE a.docstatus != 2
        """,
        as_dict=1,
    )

    # Generate period list
    period_list = get_period_list(filters)

    # Populate data
    for cost in cost_centers:
        center = {"cost_center": cost.get("cost_center")}

        for period in period_list:
            query = f"""
            SELECT SUM(b.net_total) AS total
            FROM `tabPurchase Invoice Item` a
            INNER JOIN `tabPurchase Invoice` b ON a.parent = b.name
            WHERE b.docstatus != 2
              AND b.cost_center = '{cost.get('cost_center')}'
              AND {where_clause}
              AND b.posting_date BETWEEN '{period.get('from_date')}' AND '{period.get('to_date')}'
            """
            result = frappe.db.sql(query, as_dict=1)
            center[period.get("key")] = flt(result[0].get("total") if result else 0)

        # Calculate total for the cost center
        center["total"] = sum(value for key, value in center.items() if isinstance(value, (int, float)))
        data.append(center)

    return data


def get_columns(filters):
    """
    Defines the columns for the report.
    """
    period_list = get_period_list(filters)
    columns = [
        {
            "label": _("Cost Center"),
            "fieldname": "cost_center",
            "fieldtype": "Link",
            "options": "Cost Center",
            "width": 300,
        }
    ]

    for period in period_list:
        columns.append(
            {
                "label": period["label"],
                "fieldname": period["key"],
                "fieldtype": "Currency",
                "options": "currency",
                "width": 150,
            }
        )

    columns.append(
        {
            "label": _("Total"),
            "fieldname": "total",
            "fieldtype": "Currency",
            "options": "currency",
            "width": 150,
        }
    )

    return columns


def execute(filters=None):
    """
    Executes the report generation.
    """
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data
