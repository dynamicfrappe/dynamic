frappe.views.calendar["Actions"] = {
  field_map: {
    start: "date",
    end: "date",
    id: "name",
    title: "name",
    allDay: "allDay",
    
    // progress: "progress",
  },
  get_events_method: "dynamic.terra.doctype.actions.actions.get_events",

};