frappe.ui.form.on("Payment Entry", {
  
  paid_amount:(frm)=>{
    frappe.call({
      method: "dynamic.api.get_active_domains",
      callback: function (r) {
        if (r.message && r.message.length) {
          if (r.message.includes("Payment Deduction")) {
            frm.events.get_deduct_amount(frm);
          }  
          }
      }
  })
  },
  mode_of_payment:(frm)=>{
    frappe.call({
      method: "dynamic.api.get_active_domains",
      callback: function (r) {
        if (r.message && r.message.length) {
          if (r.message.includes("Payment Deduction")) {
            if(frm.doc.mode_of_payment !=''){
              frm.events.get_deduct_amount(frm);
              frappe.call({
              "method":"dynamic.api.validate_mode_of_payment_naming",
              args:{
                  old_naming:frm.doc.mode_of_payment_naming,
                  mode_of_payment:frm.doc.mode_of_payment
              },callback(r){
                  if(!r.message){
                      frm.set_value("mode_of_payment",'');
                      frappe.throw(__("Different naming template"))
                  }
              }
          })
          }
          }  
          }
      }
  })
      
  },
  get_deduct_amount:(frm)=>{
    cur_frm.clear_table("taxes");
    frm.refresh_fields("taxes");
    frappe.call({
        "method": "frappe.client.get",
            args: {
                doctype: "Mode of Payment",
                name: frm.doc.mode_of_payment
            },callback(r){
                if(r.message){
                    let res = r.message;
                    if(res.has_deduct){
                        var row = cur_frm.add_child("taxes")
                        row.charge_type = "Actual";
                        row.account_head = res.recived_account;
                        row.description = res.recived_account;
                        // row.percentage = res.deduct_percentage;
                        //row.cost_center = res.cost_center
                        row.rate =res.deduct_percentage; //frm.doc.paid_amount * (res.deduct_percentage/100);
                        row.tax_amount = frm.doc.paid_amount * (res.deduct_percentage/100);
                        frm.refresh_fields("taxes");
                    }
                }
            }
    })
  },

  paid_from:function(frm) {
    frm.doc.currency_exchange =1
    frm.set_df_property("currency_exchange" , "hidden" , 1) 
    var account = frm.doc.paid_from 
    var currency = frm.doc.paid_from_account_currency 
    if (currency != frappe.get_doc(":Company", frm.doc.company).default_currency ) {
      frappe.call({
        "method" :"dynamic.dynamic.utils.currency_valuation_rate" ,
         async: false,
        "args" :{
          "account" : account
        },callback :function(r){
         if (r.message) {
          frm.doc.currency_exchange = r.message
          frm.set_df_property("currency_exchange" , "hidden" , 0) 
          frm.refresh_field("currency_exchange")
         }
         
        }
      })
      
    }

  },
  // setup: function (frm) {
  //   frm.set_query("drawn_bank_account", function () {
  //     return {
  //       filters: [
  //         // ["bank", "=", frm.doc.drawn_bank],
  //         ["is_company_account", "=", 1],
  //       ],
  //     };
  //   });
  //   // frm.set_query("endorsed_party_account", function () {
  //   //   return {
  //   //     filters: [
  //   //       ["company", "=", frm.doc.company],
  //   //       ["is_group", "=", 0],
  //   //       ["disabled", "=", 0],
  //   //     ],
  //   //   };
  //   // });
  // },
  get_party_account_ch: function (frm, callback) {
    if (
      frm.doc.company &&
      frm.doc.endorsed_party_type &&
      frm.doc.endorsed_party_name
    ) {
      frappe.call({
        method: "erpnext.accounts.party.get_party_account",
        args: {
          party_type: frm.doc.endorsed_party_type,
          party: frm.doc.endorsed_party_name,
          company: frm.doc.company,
        },
        callback: (response) => {
          if (response) callback(response);
        },
      });
    }
  },
  endorsed_party_name: function (frm) {
    frm.events. get_party_account_ch(frm, function (r) {
      if (r.message) {
        frm.set_value("endorsed_party_account", r.message);
      }
    });
  },
  target_exchange_rate(frm){
    // if (frm.doc.target_exchange_rate != 1) {
    //   var paid_amount = frm.doc.target_exchange_rate * frm.doc.received_amount
    //   frm.set_value("paid_amount",paid_amount)
    //   frm.refresh_field("paid_amount")
    //   console.log("hellow",paid_amount)
    // }
   
  },
  refresh(frm) {
    console.log(11)
    // your code here
    if (frm.doc.docstatus == 1 && frm.doc.cheque) {
      frm.events.add_cheque_buttons(frm);
    }
    if(frm.doc.is_from_cheque_submission){
      frm.set_df_property("cheque" , "hidden" , 0) 
      frm.set_df_property("cheque_status" , "hidden" , 0) 
      frm.set_df_property("endorse_cheque" , "hidden" , 0)
    }
    if(frm.doc.cheque_status == "Under Collect"){
      frm.set_df_property("cash_mod_of_payment" , "hidden" , 0)
    }
    else{
      frm.set_df_property("cash_mod_of_payment" , "hidden" , 1)
    }
  },
  add_cheque_buttons(frm) {
    if (frm.doc.payment_type == "Pay" && frm.doc.cheque_status == "New") {
      frm.add_custom_button(
        __("Pay"),
        function () {
          // frm.events.add_row_cheque_tracks(frm,'Paid')
          frm.events.make_cheque_pay(frm);
        },
        __("Cheque Management")
      );
      //** replace cheque by cash */
      frm.add_custom_button(
        __("Cash"),
        function(){
          frm.events.pay_cash_new(frm)
        },
        __("Cheque Management")
      );
      
    }
    if (frm.doc.payment_type == "Receive") {
      if (["New"].includes(frm.doc.cheque_status)) {
        // cheque Endorsement
        frm.add_custom_button(
          __("Endorsement"),
          function () {
            frm.events.make_cheque_endorsement(frm);
          },
          __("Cheque Management")
        );
        // Collections Cheque Now
        frm.add_custom_button(
          __("Collect Now"),
          function () {
            frm.events.collect_cheque_now(frm);
          },
          __("Cheque Management")
        );
        // deposite Cheque under collcttion
        frm.add_custom_button(
          __("Deposit Under Collection"),
          function () {
            frm.events.deposite_cheque_under_collection(frm);
          },
          __("Cheque Management")
        );
      }
      if (["New"].includes(frm.doc.cheque_status)) {
      }

      // cheque under collction

      if (["Under Collect"].includes(frm.doc.cheque_status)) {
        frm.add_custom_button(
          __("Collect"),
          function () {
            frm.events.collect_cheque_under_collection(frm);
          },
          __("Cheque Under Collection")
        );
        //** replace cheque by cash */
        frm.add_custom_button(
          __("Cash"),
          function(){
            frm.events.pay_cash_new(frm)
          },
          __("Cheque Under Collection")
        );
        frm.add_custom_button(
          __("Reject"),
          function () {
            frm.events.reject_cheque_under_collection(frm);
          },
          __("Cheque Under Collection")
        );
        frm.add_custom_button(
          __("Reject Cheque In Bank"),
          function () {
            frm.events.add_row_cheque_tracks(frm,"Rejected In Bank")
          },
          __("Cheque Under Collection")
        );
        // return_cheque_xx
        frm.add_custom_button(
          __("Return Cheque"),
          function () {
            frm.events.return_cheque(frm);
          },
          __("Cheque Under Collection")
        );
      }

      // Reject cheque under collction
      if (["Rejected in Bank"].includes(frm.doc.cheque_status)) {
        // deposite Cheque under collcttion
        frm.add_custom_button(
          __("Deposit Under Collection"),
          function () {
            frm.events.deposite_cheque_under_collection(frm);
          },
          __("Cheque Management")
        );
      }

      
    }
  },
  make_cheque_endorsement(frm) {
    if (!frm.doc.drawn_bank_account) {
      frappe.throw(__("Please Set Bank Account"));
    }
    frappe.call({
      method: "dynamic.cheques.doctype.cheque.cheque.make_cheque_endorsement",
      args: {
        payment_entry: frm.doc.name,
      },
      callback: function (r) {
        frm.refresh();
        if (r && r.message) {
          frappe.set_route("Form", r.message.doctype, r.message.name);
        }
      },
    });
  },
  collect_cheque_now(frm) {
    frappe.call({
      method: "dynamic.cheques.doctype.cheque.cheque.collect_cheque_now",
      args: {
        payment_entry: frm.doc.name,
      },
      callback: function (r) {
        frm.refresh();
        if (r && r.message) {
          frappe.set_route("Form", r.message.doctype, r.message.name);
        }
      },
    });
  },
  deposite_cheque_under_collection(frm) {
    frappe.call({
      method:
        "dynamic.cheques.doctype.cheque.cheque.deposite_cheque_under_collection",
      args: {
        payment_entry: frm.doc.name,
      },
      callback: function (r) {
        frm.refresh();
        if (r && r.message) {
          frappe.set_route("Form", r.message.doctype, r.message.name);
        }
      },
    });
  },
  return_cheque(frm) {
    frappe.call({
      method:
        "dynamic.cheques.doctype.cheque.cheque.return_cheque",
      args: {
        payment_entry: frm.doc.name,
      },
      callback: function (r) {
        // frm.refresh();
        if (r && r.message) {
          frappe.set_route("Form", r.message.doctype, r.message.name);
        }
      },
    });
  },
  collect_cheque_under_collection(frm) {
    frappe.call({
      method:
        "dynamic.cheques.doctype.cheque.cheque.collect_cheque_under_collection",
      args: {
        payment_entry: frm.doc.name,
      },
      callback: function (r) {
        frm.refresh();
        if (r && r.message) {
          frappe.set_route("Form", r.message.doctype, r.message.name);
        }
      },
    });
  },
  reject_cheque_under_collection(frm) {
    frappe.call({
      method:
        "dynamic.cheques.doctype.cheque.cheque.reject_cheque_under_collection",
      args: {
        payment_entry: frm.doc.name,
      },
      callback: function (r) {
        frm.refresh();
        if (r && r.message) {
          frappe.set_route("Form", r.message.doctype, r.message.name);
        }
      },
    });
  },
  make_cheque_pay(frm) {
    if (!frm.doc.drawn_bank_account) {
      frappe.throw(__("Please Set Bank Account"));
    }
    frappe.call({
      method: "dynamic.cheques.doctype.cheque.cheque.make_cheque_pay",
      args: {
        payment_entry: frm.doc.name,
      },
      callback: function (r) {
        frm.refresh();
        if (r && r.message) {
          frappe.set_route("Form", r.message.doctype, r.message.name);
        }
      },
    });
  },
  add_row_cheque_tracks(frm,new_cheque_status) {
    // if (!frm.doc.drawn_bank_account) {
    //   frappe.throw(__("Please Set Bank Account"));
    // }
    frappe.call({
      method:"dynamic.cheques.doctype.cheque.cheque.add_row_cheque_tracks",
      args:{
        payment_entry:frm.doc.name,
        new_cheque_status:new_cheque_status
      },
      callback:function(r){
        if(!r.exc){
          frm.refresh()
        }else{
          frappe.throw(r.exc)
        }
      }
    })
  },
  pay_cash_new(frm){
    if (!frm.doc.cash_mod_of_payment) {
      frappe.throw(__("Please Add Cash Mode Of Payment"));
    }
    frappe.call({
      method:"dynamic.cheques.doctype.cheque.cheque.pay_cash_new",
      args:{
        payment_entry : frm.doc.name,
      },
      callback:function(r){
        if(!r.exc){
          frm.refresh()
          frappe.set_route("Form", r.message.doctype, r.message.name);
        }else{
          frappe.throw(r.exc)
        }
      }
    })
  }
});
