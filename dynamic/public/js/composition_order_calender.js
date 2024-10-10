frappe.views.calendar["Composition Order"] = {
    field_map: {
        start: "start",
        end: "end",
        id: "name",
        title: "name",
        allDay: "allDay",
    },
  get_events_method: "dynamic.logistics.doctype.composition_order.composition_order.get_events",
};
