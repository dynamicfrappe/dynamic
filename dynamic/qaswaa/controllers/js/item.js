frappe.ui.form.on('Item', {
    refresh:function(frm){
        frappe.call({
            method: "dynamic.api.get_active_domains",
            callback: function (r) {
                if (r.message && r.message.length) {
                    if (r.message.includes("Item Integration")) {
                        console.log("helloo");
                        frm.events.transfer_item(frm);
                    }
                }
            }
        })
    },
    item_group: function (frm){
        frm.events.check_url(frm);
        console.log("hehehee");
},
transfer_item(frm){
    frm.add_custom_button(__('Send Item'), () => {
        console.log("Item Sent");
        console.log(frm.doc);
        
        
        frappe.call({
            method: "dynamic.qaswaa.controllers.item.after_insert",
            args:{
                self:frm.doc,
            },
            callback: function (r) {
                console.log(r.message);
            }
        })
    });
        
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