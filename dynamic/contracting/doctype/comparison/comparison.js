// Copyright (c) 2021, Dynamic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Comparison', {
    validate_customer:(frm)=>{
        let customer   = frm.doc.customer
        let contractor = frm.doc.contractor
        if(customer == contractor){
            frm.set_value("customer","");
            frm.set_value("customer_name","");
            frm.set_value("contractor","");
            frm.set_value("contractor_name","");
            frappe.throw("Customer Must Be different Than Contractor")
        }
     },
    customer:(frm)=>{
        if(frm.doc.customer != "") {
            frm.events.validate_customer(frm);
        }
    },
    contractor:(frm)=>{
        if(frm.doc.contractor) {
            frm.events.validate_customer(frm);
        }
    },
	start_date:function(frm){
        let start_date = new Date(frm.doc.start_date)
        let end_date = new Date(frm.doc.end_date)
        let now = new Date()
        start_date.setDate(start_date.getDate() + 1)
        if(start_date < now){
            frm.set_value("start_date","")
            frappe.throw("Start Date Should Be After Today")
        }
        if(end_date < start_date){
            frm.set_value("start_date","")
            frm.set_value("end_date","")
            frappe.throw("End Date Must be After Start Date")
        }
    },
    end_date:function(frm){
        let start_date = new Date(frm.doc.start_date)
        let end_date = new Date(frm.doc.end_date)
        if(end_date <start_date){
            frm.set_value("start_date","")
            frm.set_value("end_date","")
            frappe.throw("End Date Must be After Start Date")
        }
    },
    purchase_taxes_and_charges_template:(frm)=>{
        let tax_temp = frm.doc.purchase_taxes_and_charges_template
        if(tax_temp !=null){
            frappe.call({
                method: "frappe.client.get",
                args: {
                  doctype: "Purchase Taxes and Charges Template",
                  name: tax_temp,
                },
                callback: function (r) {
                  if (r.message) {
                    let taxes = r.message["taxes"]
                      //console.log("rrrrrrrrrr",taxes)
                      for(let i=0 ; i<taxes.length ; i++){
                          let row = cur_frm.add_child("taxes")
                          row.charge_type = taxes[i].charge_type
                          row.account_head = taxes[i].account_head
                          row.rate = taxes[i].rate
                          row.tax_amount = ((taxes[i].rate/100) * frm.doc.total_price) || 0
                          row.total = (((taxes[i].rate/100) * frm.doc.total_price) + frm.doc.grand_total) || 0
                          row.description = taxes[i].description
                      }
                      cur_frm.refresh_fields("taxes");
                      frm.events.clac_taxes(frm);
                  }
                },
              });
        }

    },
    clac_taxes:(frm)=>{
        let items  = frm.doc.item || []
        let taxes = frm.doc.taxes || []
        let totals = 0
        let total_qty = 0
        let totals_after_tax = 0
        let total_tax_rate = 0
        let total_tax = 0
        let tax_table = []
        for(let i=0 ; i< items.length ; i++){
            totals += parseFloat(items[i].total_price || 0)
            total_qty += parseInt(items[i].qty || 0)
        }

        let tax_v = parseFloat(totals || 0)
        for(let i=0;i<taxes.length;i++){
            total_tax_rate += taxes[i].rate
            taxes[i].tax_amount = (taxes[i].rate  / 100) *  totals
            tax_v +=parseFloat(taxes[i].tax_amount)
            //taxes[i].total = (taxes[i].rate  / 100) *  totals + totals
            if(i==0) {
                taxes[i].total =tax_v //(taxes[i].rate  / 100) * totals + totals
            }else{
                taxes[i].total = tax_v//(taxes[i-1].total || totals) + taxes[i].tax_amount
            }
            tax_table.push(taxes[i])
        }

        total_tax = (totals * (total_tax_rate/100))
          totals_after_tax = parseFloat(totals) + parseFloat(total_tax)
         //////  clear child table and add row from scratch to update amount value
         cur_frm.clear_table("taxes")
         for(let i=0 ; i<tax_table.length ; i++){
              let row = cur_frm.add_child("taxes")
              row.charge_type = tax_table[i].charge_type
              row.account_head = tax_table[i].account_head
              row.rate = tax_table[i].rate
              row.tax_amount = tax_table[i].tax_amount
              row.total = tax_table[i].total
         }

         ////// calc insurance
         let insurance_value = (totals_after_tax * (frm.doc.insurance_value_rate)/100)
         let delivery_value  = (totals_after_tax * (frm.doc.delevery_insurance_value_rate_)/100)
         let total_ins =  insurance_value +  delivery_value
         frm.set_value("total_insurance",parseFloat(total_ins))
         frm.set_value("insurance_value",parseFloat(insurance_value))
         frm.set_value("delivery_insurance_value",parseFloat(delivery_value))
         frm.refresh_fields("taxes")
         frm.set_value("total_qty",parseFloat(total_qty))
         frm.set_value("total_price",parseFloat(totals))
         frm.set_value("tax_total",parseFloat(total_tax))
         frm.set_value("total",parseFloat(totals_after_tax))
         frm.set_value("grand_total",parseFloat(totals_after_tax))
         frm.refresh_field("total_qty")
         frm.refresh_field("total_price")
         frm.refresh_field("tax_total")
         frm.refresh_field("grand_total")
         frm.refresh_field("total")
         frm.refresh_field("total_insurance")


    },
    validate:(frm)=>{
        if(frm.doc.bank_guarantee !="") {
            frappe.call({
                method: "frappe.client.get",
                args: {
                    doctype: "Bank Guarantee",
                    name: frm.doc.bank_guarantee,
                },
                callback: function (r) {
                    if (r.message) {
                       let obj =r.message
                        if(frm.doc.customer != obj.customer && frm.doc.comparison_type =="Direct"){
                            frm.set_value("bank_guarantee","")
                            frappe.throw("Invalid Customer In Bank Guarantee")
                        }
                        if(frm.doc.contractor != obj.customer && frm.doc.comparison_type =="From Contractor"){
                           frm.set_value("bank_guarantee","")
                            frappe.throw("Invalid Customer In Bank Guarantee")
                        }
                        if(Math.ceil(frm.doc.total_insurance) != Math.ceil(obj.amount)){
                            frappe.throw("Invalid Amount In Bank Guarantee")
                        }
                    }
                },
            });
        }
    },
    insurance_value_rate:(frm)=>{
        let insurance_value_rate = frm.doc.insurance_value_rate
        let ins_value   = frm.doc.grand_total * (insurance_value_rate/100)
        let total_ins   = ins_value + (frm.doc.delivery_insurance_value || 0)
        frm.set_value("insurance_value",ins_value)
        frm.set_value("total_insurance",total_ins)
    },
    delevery_insurance_value_rate_:(frm)=>{
        let delivery_ins_rate = frm.doc.delevery_insurance_value_rate_
        let delivery_ins_value = frm.doc.grand_total * (delivery_ins_rate/100)
         let total_ins   = delivery_ins_value + (frm.doc.insurance_value || 0)
        frm.set_value("delivery_insurance_value",delivery_ins_value)
        frm.set_value("total_insurance",total_ins)
    }
});

frappe.ui.form.on('Clearance Items', {
        clearance_item:(frm,cdt,cdn)=>{
            var  local = locals[cdt][cdn]
            if(local.clearance_item !=null ){
            frappe.call({
                method:"dynamic.contracting.doctype.comparison.comparison.get_item_price",
                args:{
                    "item_code":local.clearance_item
                },
                callback(r){
                    if(r.message){
                        local.price = r.message
                        if(local.qty){
                            local.total_price = local.qty * r.message
                        }
                        frm.refresh_fields("item")
                    }
                }
            })
           }
        },
        qty:(frm,cdt,cdn)=>{
            let local = locals[cdt][cdn]
            if(local.qty && local.price){
                local.total_price = local.qty * local.price
                frm.events.clac_taxes(frm);
                frm.refresh_fields("item")
            }
        },
    price:(frm,cdt,cdn)=>{
        let local = locals[cdt][cdn]
        local.total_price = (local.price * local.qty) || 0
        frm.refresh_fields("item")
        frm.events.clac_taxes(frm);
    },
   item_remove:(frm,cdt,cdn)=>{
        frm.events.clac_taxes(frm);
    }

})
frappe.ui.form.on('Purchase Taxes and Charges Clearances', {
	rate:(frm,cdt,cdn)=>{
        frm.events.clac_taxes(frm);
    },
    taxes_remove:(frm,cdt,cdn)=>{
        frm.events.clac_taxes(frm);
    },
    taxes_add:(frm,cdt,cdn)=>{
        var row = locals[cdt][cdn]
        if(row.rate) {
            frm.events.clac_taxes(frm);
        }
    }
})