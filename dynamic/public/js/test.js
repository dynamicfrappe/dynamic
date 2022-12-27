frappe.views.calendar['Appointment'] = {
    field_map: {
        "start": "start",
        "end": "end",
        "id": "name",
        "title": "description",
        "allDay": "allDay",
    },


gantt: true,

// filters: [test
//     {
//         "fieldtype": "Link",
//         "fieldname": "sales_order",
//         "options": "Sales Order",
//         "label": __("Sales Order")
//     },
// ],/home/abanoub/frappe-13/apps/dynamic/dynamic/ifi/api.py
get_events_method: "dynamic.ifi.api.get_events",

// get_css_class: function(data) {
//     // console.log(data)
//     if(data.ref_status=="Pending") {
//         return "success";
//     } if(data.ref_status=="Start") {
//         return "danger";
//     } else if(data.ref_status=="Inprogress") {
//         return "warning";
//     } else if(data.ref_status=="Completed") {
//         return "extra-light";
//     }
// },
}

