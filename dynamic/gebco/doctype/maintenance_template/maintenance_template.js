// Copyright (c) 2022, Dynamic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Maintenance Template', {
    refresh: function(frm) {
        // if(frm.doc.__islocal ==0){
        //     if(frm.doc.)
        // }
    }
});

frappe.ui.form.on('Cars Plate Numbers For Template', {
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

frappe.ui.form.on('Maintenance Team', {
    employee: (frm, cdt, cdn) => {
        let row = locals[cdt][cdn]
        let employees = frm.doc.maintenance_team
        let count = 0
        for (let i = 0; i < employees.length; i++) {
            if (employees[i].employee == row.employee) {
                count += 1
                if (count > 1) {
                    row.employee = ""
                    frappe.msgprint("This Employee Already Exist")
                }
            }
        }
    }
})