frappe.ui.form.on("Sales Invoice", {
  refresh(frm) {
    // your code here
    frm.events.setDateTimeIssued(frm);
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
            d.itemcode = `EGS-${r.message.tax_id || ''}-${d.item_code || ''}`;
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
