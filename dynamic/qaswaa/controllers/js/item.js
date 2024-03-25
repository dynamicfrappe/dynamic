frappe.ui.form.on('Item', {
    item_group: function (frm){
        frm.events.check_url(frm);
        console.log("hehehee");
},
check_url: function (frm) {
        
        frappe.call({
            method: "dynamic.api.get_active_domains",
            callback: function (r) {
                if (r.message && r.message.length) {
                    if (r.message.includes("Qaswaa")) {
                        frm.events.event_trger(frm);
                    }
                }
            }
        })
    
},
event_trger: function(frm) {
		let item_group = frm.doc.item_group;
		if(item_group){
		     frappe.call({
                method: "frappe.client.get",
                args: {
                    doctype: "Item Group",
                    name: item_group,
                },
                callback: function(r) {
                    let group_code = r.message.group_code ;
                    frm.set_value("group_code" , group_code);
                    refresh_field("group_code");
                }
            });
		}
	}
})