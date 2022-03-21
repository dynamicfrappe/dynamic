// Copyright (c) 2022, Dynamic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Maintenance Contract', {
    refresh: function(frm) {
        if (frm.doc.docstatus == 0) {
            console.log("from if")
            frm.add_custom_button(__("Renew"), function() {
                //console.log("renew")
                frappe.model.open_mapped_doc({
                    method: "dynamic.gebco.doctype.maintenance_contract.maintenance_contract.renew_contract",
                    frm: frm,
                });
            });
        }
    }
});

frappe.ui.form.on('Cars Plate Numbers', {
    plate_number: (frm, cdt, cdn) => {
        let row = locals[cdt][cdn]
        console.log(row.plate_number)
        if (row.plate_number.length > 1) {
            let count = 0
            for (let i = 0; i < frm.doc.cars_plate_numbers.length; i++) {
                if (frm.doc.cars_plate_numbers[i].plate_number == row.plate_number) {

                    count += 1
                    if (count > 1) {
                        row.plate_number = ""
                        frappe.msgprint("This Plate Number Already Exist")
                    }
                }
            }
        }
    }
})