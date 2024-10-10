frappe.views.calendar["Conservation order"] = {
    field_map: {
        start: "start",
        end: "end",
        id: "name",
        title: "name",
        allDay: "allDay",
    },
  get_events_method: "dynamic.logistics.doctype.conservation_order.conservation_order.get_events",
};
