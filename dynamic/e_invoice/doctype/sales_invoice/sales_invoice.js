var message = "";

function socket(action) {
  var minus = 1,
    plus = 2,
    value = 3,
    users = 3,
    websocket = new WebSocket("ws://127.0.0.1:6789/");
  var run_1 = function (action) {
    try {
      websocket.onopen = function (evt) {
        try {
          websocket.send(action);
        } catch (err) {
          console.log("error");
        }
      };
    } catch (err) {
      frappe.show_alert("No Token", 5);
    }
  };
  function plus() {
    websocket.send(JSON.stringify({ action: "plus" }));
  }

  websocket.onmessage = function (event) {
    message = event.data;
    var data = JSON.parse(message);
    console.log("data ===> ", data);
    if (data.status) {
      frappe.show_alert({ message: data.status, indicator: "blue" });
      message = data.status;
      if (data.response) {
        frappe.call({
          method:
            "dynamic.e_invoice.doctype.sales_invoice.sales_invoice_fun.update_invoice_submission_status",
          args: {
            submit_response: data.response,
          },
          callback: function (r) {
            // cur_frm.events.get_document_sinv(cur_frm);
            window.location.reload();
          },
        });
      }

      return message;
    }
  };

  run_1(action);
}

frappe.ui.form.on("Sales Invoice", {
  domian_valid: function (frm) {
    var tera = false
   frappe.call({
         method :"dynamic.dynamic.validation.get_active_domain_gebco" ,
         async: false,
         callback:function (r){
             if (r.message) {
                 tera = true
             }else {
                 tera = false
             }
         }
     })
  return tera
} ,
  onload(frm) {
    var check_domain = frm.events.domian_valid()
    console.log(check_domain)
    if (!check_domain){
      console.log("ONE")
    frm.events.add_e_tax_btns(frm); } 
    if (check_domain && frm.doc.docstatus == 0) {
      frm.add_custom_button(
        __("view Item Shortage"),
        function () {
          frappe.call({
            method:
              "dynamic.api.validate_active_domains_invocie",
            args: {
              doc: frm.doc ,
            },
            callback: function (r) {
               console.log(r.message);
              
              // socket(JSON.stringify(data));
            },
          });
        },
        "view Item Shortage"
      );
    }
  },
  after_save(frm) {
    frm.events.add_e_tax_btns(frm);
  },
  refresh(frm) {
    if (frm.is_new()) {
      frm.doc.submission_id = "";
      frm.doc.uuid = "";
      frm.doc.long_id = "";
      frm.doc.error_code = "";
      frm.doc.error_details = "";
      frm.doc.invoice_status = "";
    }
    var check_domain = frm.events.domian_valid()
    if (check_domain && frm.doc.docstatus == 0 ){
      frm.add_custom_button(
        __("view Item Shortage"),
        function () {
          frappe.call({
            method:
              "dynamic.api.validate_active_domains_invocie",
            args: {
              doc: frm.doc.name ,
            },
            callback: function (r) {
               console.log(r.message);
              
              // socket(JSON.stringify(data));
            },
          });
        },
        "view Item Shortage"
      );

    }else {
    // your code here

    frm.events.setDateTimeIssued(frm);
    frm.set_query("branch", () => {
      return {
        filters: [["company", "=", frm.doc.company]],
      };
    });

    var data = { name: "ahmed" };
    socket(JSON.stringify(data)); 
  }
  },

  add_e_tax_btns(frm) {
    var data = { name: "ahmed" };
    socket(JSON.stringify(data));
    // if (frm.doc.docstatus == 1 && frm.doc.is_send == 0) {
    // if (frm.doc.docstatus == 1) {
    if (message == "Token connecting" || message == "success") {
      frm.events.add_post(frm);
    }
    frm.events.add_check_token(frm);

    if (frm.doc.uuid) {
      frm.events.add_get_document(frm);
    }
  },

  add_check_token(frm) {
    frm.add_custom_button(
      __("Check Token"),
      function () {
        var data = { name: "ahmed" };
        socket(JSON.stringify(data));
        if (message == "Token connecting" || message == "success") {
          frm.events.add_post(frm);
        } else {
          frappe.show_alert({ message: "no connection", indicator: "red" });
        }
      },
      __("E Tax")
    );
  },
  add_post(frm) {
    if (["Invalid", ""].includes(frm.doc.invoice_status || "")) {
      frm.add_custom_button(
        __("POST TO TAX"),
        function () {
          frappe.call({
            method:
              "dynamic.e_invoice.doctype.sales_invoice.sales_invoice_fun.post_sales_invoice",
            args: {
              invoice_name: frm.doc.name,
            },
            callback: function (r) {
              // console.log(r.message);
              var data = r.message;
              socket(JSON.stringify(data));
            },
          });
        },
        "E Tax"
      );
    }
  },

  add_get_document(frm) {
    frm.add_custom_button(
      __("Document Status"),
      function () {
        frm.events.get_document_sinv(frm);
      },
      "E Tax"
    );
  },

  get_document_sinv(frm) {
    frappe.call({
      method:
        "dynamic.e_invoice.doctype.sales_invoice.sales_invoice_fun.get_document_sales_invoice",
      args: {
        invoice_name: frm.doc.name,
      },
      callback: function (r) {
        window.location.reload();
      },
    });
  },
  tax_auth(frm) {
    //   if (frm.doc.tax_auth) {
    let df = frappe.meta.get_docfield(
      "Sales Invoice",
      "date_issued",
      me.frm.doc.name
    );
    if (df) {
      df.reqd = frm.doc.tax_auth == 1;
      frm.refresh_field("date_issued");
    }

    //   }
  },
  date_issued(frm) {
    frm.events.setDateTimeIssued(frm);
  },
  setDateTimeIssued(frm) {
    if (frm.doc.date_issued) {
      frm.doc.datetime_issued = toISOString(
        String(new Date(frm.doc.date_issued))
      );
      var tzoffset = new Date().getTimezoneOffset() * 60000;
      frm.refresh_field("datetime_issued");
    }
  },
  validate(frm) {
    frm.events.calculate_item_taxes(frm);
  },
  calculate_item_taxes(frm) {
    if (frm.doc.items) {
      frm.doc.items.forEach((d) => {
        if (d.tax_amount) {
          d.tax_rate = (d.tax_amount / (d.amount || 1)) * 100;
        } else if (d.tax_rate) {
          d.tax_amount = (d.amount * d.tax_rate) / 100;
        } else {
          d.tax_amount = 0;
          d.tax_rate = 0;
        }
      });
    }
    frm.refresh_field("items");
  },
});

frappe.ui.form.on("Sales Invoice Item", {
  tax_rate(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    if (d.tax_rate && d.amount) {
      d.tax_amount = (d.amount * d.tax_rate) / 100;
    } else {
      d.tax_amount = 0;
      d.tax_rate = 0;
    }
    frm.refresh_field("items");
  },
  tax_amount(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    if (d.tax_amount && d.amount) {
      d.tax_rate = (d.tax_amount / (d.amount || 1)) * 100;
    } else {
      d.tax_amount = 0;
      d.tax_rate = 0;
    }
    frm.refresh_field("items");
  },
  rate(frm, cdt, cdn) {
    frm.events.calculate_item_taxes(frm);
  },
  amount(frm, cdt, cdn) {
    frm.events.calculate_item_taxes(frm);
  },
  qty(frm, cdt, cdn) {
    frm.events.calculate_item_taxes(frm);
  },
  item_code(frm, cdt, cdn) {
    frm.events.calculate_item_taxes(frm);
  },
  item_type(frm, cdt, cdn) {
    //   if (frm.doc.tax_auth) {
    var d = locals[cdt][cdn];
    if (d.item_type == "EGS") {
      frappe.call({
        method: "frappe.client.get",
        args: {
          doctype: "Company",
          name: frappe.defaults.get_default("company"),
        },
        callback: function (r) {
          if (r.message) {
            d.itemcode = `EGS-${r.message.tax_id || ""}-${d.item_code || ""}`;
          }
          frm.refresh_field("items");
        },
      });
    }
    frm.refresh_field("items");

    //   }
  },
});

var toISOString = function (s) {
  let months = {
    jan: "01",
    feb: "02",
    mar: "03",
    apr: "04",
    may: "05",
    jun: "06",
    jul: "07",
    aug: "08",
    sep: "09",
    oct: "10",
    nov: "11",
    dec: "12",
  };
  let b = s.split(" ");
  // alert(b)
  return (
    b[3] +
    "-" +
    months[b[1].toLowerCase()] +
    "-" +
    ("0" + b[2]).slice(-2) +
    "T" +
    b[4] +
    "Z"
  );
};
