

frappe.ui.form.on('Pricing Rule Item Code', {
    item_code: function(frm, cdt, cdn) {
        console.log('item_code trigger fired');

        let row = locals[cdt][cdn];
        if (row.item_code) {
            frappe.db.get_doc('Item', row.item_code).then(doc => {
                console.log('Item fetched:', doc);
                frappe.model.set_value(cdt, cdn, 'unit_floor', doc.unit_floor);
                frappe.model.set_value(cdt, cdn, 'unit_area1', doc.unit_area);
                frm.refresh_field('pricing_rule_items'); // استبدل بالاسم الصحيح للـ child table
            }).catch(error => {
                console.log('Error:', error);
                frappe.msgprint(__('Error fetching item details.'));
            });
        }
    }
});



