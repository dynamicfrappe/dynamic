// Copyright (c) 2024, Dynamic and contributors
// For license information, please see license.txt

// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt


// {% include 'erpnext/selling/sales_common.js' %}

frappe.ui.form.on('Pre Quotation', {
	onload:function(frm){

	},
	refresh:function(frm){
		frm.trigger("set_label");
	 	frm.trigger("set_dynamic_field_label");
		frm.events.upload_data_file(frm)
		frm.fields_dict["items"].grid.add_custom_button(
			__("Export Excel"),
			function() {
			  // console.log("frm.items");
			  frappe.call({
				method: "dynamic.api.export_data_to_csv_file",
				args: {
				  items: frm.doc.items,
				},
				callback: function(r) {
				  if (r.message){
					  let file = r.message.file 
					  let file_url = r.message.file_url 
					  file_url = file_url.replace(/#/g, '%23');
					  window.open(file_url);
				  }
				},
			  });
	  
			}
		  );
	},
	upload_data_file:function(frm){
		frm.fields_dict["items"].grid.add_custom_button(
		  __("Upload Xlxs Data"),
		  function() {
			  let d = new frappe.ui.Dialog({
				  title: "Enter details",
				  fields: [
					{
					  label: "Excel File",
					  fieldname: "first_name",
					  fieldtype: "Attach",
					},
				  ],
				  primary_action_label: "Submit",
				  primary_action(values) {
					console.log(`values===>${JSON.stringify(values)}`);
					var f = values.first_name;
					frappe.call({
					  method:"dynamic.api.get_data_from_template_file",
					  args: {
						file_url: values.first_name
						// file: values.first_name,
						// colms:['item_code','qty',]
					  },
					  callback: function(r) {
						if (r.message) {
						  console.log(r.message)
						  frm.clear_table("items");
						  frm.refresh_fields("items");
						  r.message.forEach(object => {
							var row = frm.add_child("items");
							Object.entries(object).forEach(([key, value]) => {
							  //  console.log(`${key}: ${value}`);
							  row[key] = value;
							});
						   });
						  frm.refresh_fields("items");
						}
					  },
					});
					d.hide();
				  },
				});
				d.show();
		  }).addClass("btn-success");
		  frm.fields_dict["items"].grid.grid_buttons
		  .find(".btn-custom")
		  .removeClass("btn-default")
	},
	setup: function(frm) {
		frm.custom_make_buttons = {
			'Sales Order': 'Sales Order'
		},

		frm.set_query("quotation_to", function() {
			return{
				"filters": {
					"name": ["in", ["Customer", "Lead"]],
				}
			}
		});

		frm.set_df_property('packed_items', 'cannot_add_rows', true);
		frm.set_df_property('packed_items', 'cannot_delete_rows', true);

		frm.set_query('company_address', function(doc) {
			if(!doc.company) {
				frappe.throw(__('Please set Company'));
			}

			return {
				query: 'frappe.contacts.doctype.address.address.address_query',
				filters: {
					link_doctype: 'Company',
					link_name: doc.company
				}
			};
		});
	},
	quotation_to: function(frm) {
		frm.trigger("set_label");
		frm.trigger("toggle_reqd_lead_customer");
		frm.trigger("set_dynamic_field_label");
	},

	set_label: function(frm) {
		frm.fields_dict.customer_address.set_label(__(frm.doc.quotation_to + " Address"));
	}
});

erpnext.selling.QuotationController = erpnext.selling.SellingController.extend({
	onload: function(doc, dt, dn) {
		var me = this;
		// this._super(doc, dt, dn);

	},
	party_name: function() {
		var me = this;
		erpnext.utils.get_party_details(this.frm, null, null, function() {
			// me.apply_price_list();
			console.log("HI");
		});

		if(me.frm.doc.quotation_to=="Lead" && me.frm.doc.party_name) {
			me.frm.trigger("get_lead_details");
		}
	},
	refresh: function(doc, dt, dn) {
		// this._super(doc, dt, dn);
		doctype = doc.quotation_to == 'Customer' ? 'Customer':'Lead';
		frappe.dynamic_link = {doc: this.frm.doc, fieldname: 'party_name', doctype: doctype}

		var me = this;

		if (doc.__islocal && !doc.valid_till) {
			if(frappe.boot.sysdefaults.quotation_valid_till){
				this.frm.set_value('valid_till', frappe.datetime.add_days(doc.transaction_date, frappe.boot.sysdefaults.quotation_valid_till));
			} else {
				this.frm.set_value('valid_till', frappe.datetime.add_months(doc.transaction_date, 1));
			}
		}

		if (doc.docstatus == 1 && !["Lost", "Ordered"].includes(doc.status)) {
			if (frappe.boot.sysdefaults.allow_sales_order_creation_for_expired_quotation
				|| (!doc.valid_till)
				|| frappe.datetime.get_diff(doc.valid_till, frappe.datetime.get_today()) >= 0) {
					this.frm.add_custom_button(
						__("Sales Order"),
						this.frm.cscript["Make Sales Order"],
						__("Create")
					);
				}

			if(doc.status!=="Ordered") {
				this.frm.add_custom_button(__('Set as Lost'), () => {
						this.frm.trigger('set_as_lost_dialog');
					});
				}

			if(!doc.auto_repeat) {
				cur_frm.add_custom_button(__('Subscription'), function() {
					erpnext.utils.make_subscription(doc.doctype, doc.name)
				}, __('Create'))
			}

			cur_frm.page.set_inner_btn_group_as_primary(__('Create'));
		}

		if (this.frm.doc.docstatus===0) {
			this.frm.add_custom_button(__('Opportunity'),
				function() {
					erpnext.utils.map_current_doc({
						method: "erpnext.crm.doctype.opportunity.opportunity.make_quotation",
						source_doctype: "Opportunity",
						target: me.frm,
						setters: [
							{
								label: "Party",
								fieldname: "party_name",
								fieldtype: "Link",
								options: me.frm.doc.quotation_to,
								default: me.frm.doc.party_name || undefined
							},
							{
								label: "Opportunity Type",
								fieldname: "opportunity_type",
								fieldtype: "Link",
								options: "Opportunity Type",
								default: me.frm.doc.order_type || undefined
							}
						],
						get_query_filters: {
							status: ["not in", ["Lost", "Closed"]],
							company: me.frm.doc.company
						}
					})
				}, __("Get Items From"), "btn-default");
		}

		this.toggle_reqd_lead_customer();

	},

	set_dynamic_field_label: function(){
		if (this.frm.doc.quotation_to == "Customer")
		{
			this.frm.set_df_property("party_name", "label", "Customer");
			this.frm.fields_dict.party_name.get_query = null;
		}

		if (this.frm.doc.quotation_to == "Lead")
		{
			this.frm.set_df_property("party_name", "label", "Lead");

			this.frm.fields_dict.party_name.get_query = function() {
				return{	query: "erpnext.controllers.queries.lead_query" }
			}
		}
	},

	toggle_reqd_lead_customer: function() {
		var me = this;

		// to overwrite the customer_filter trigger from queries.js
		this.frm.toggle_reqd("party_name", this.frm.doc.quotation_to);
		this.frm.set_query('customer_address', this.address_query);
		this.frm.set_query('shipping_address_name', this.address_query);
	},

	tc_name: function() {
		this.get_terms();
	},

	address_query: function(doc) {
		return {
			query: 'frappe.contacts.doctype.address.address.address_query',
			filters: {
				link_doctype: frappe.dynamic_link.doctype,
				link_name: doc.party_name
			}
		};
	},

	validate_company_and_party: function(party_field) {
		if(!this.frm.doc.quotation_to) {
			frappe.msgprint(__("Please select a value for {0} quotation_to {1}", [this.frm.doc.doctype, this.frm.doc.name]));
			return false;
		} else if (this.frm.doc.quotation_to == "Lead") {
			return true;
		} else {
			return this._super(party_field);
		}
	},

	get_lead_details: function() {
		var me = this;
		if(!this.frm.doc.quotation_to === "Lead") {
			return;
		}

		frappe.call({
			method: "erpnext.crm.doctype.lead.lead.get_lead_details",
			args: {
				'lead': this.frm.doc.party_name,
				'posting_date': this.frm.doc.transaction_date,
				'company': this.frm.doc.company,
			},
			callback: function(r) {
				if(r.message) {
					me.frm.updating_party_details = true;
					me.frm.set_value(r.message);
					me.frm.refresh();
					me.frm.updating_party_details = false;
				}
			}
		})
	}
});

frappe.ui.form.on('Pre Quotation', {
	items :function(frm){
		let items = frm.doc.items;
		const totalQty = items.reduce((accumulator, currentValue) => {
			return accumulator + currentValue.qty;
		  }, 0);
		frm.set_value("total_qty" , totalQty);
		frm.refresh_field("total_qty");
	},
	taxes_and_charges: function(frm){
		if (frm.doc.taxes_and_charges){
			frappe.call({
				method:"dynamic.pre_quotation.doctype.pre_quotation.pre_quotation.get_taxes_and_charges",
				args: {
				  doc: frm.doc.taxes_and_charges
				},
				callback: function(r) {
					if (r.message) {
						frm.clear_table("taxes");
						frm.refresh_fields("taxes");
						r.message.forEach(object => {
							var row = frm.add_child("taxes");
							Object.entries(object).forEach(([key, value]) => {
								console.log(`${key}: ${value}`);
								row[key] = value;
							});
						});
						frm.refresh_fields("taxes");
					}
				},
			});
		}
	}
})
frappe.ui.form.on('Pre Quotation Item', {
	qty :function(frm, cdt, cdn){
		calc_amount_one_row(frm, cdt, cdn);
		update_total_qty(frm);
	},
	rate :function(frm, cdt, cdn){
		calc_amount_one_row(frm, cdt, cdn);
		update_total_amount(frm);
	},
})
function update_total_amount(frm) {
	let items = frm.doc.items || [];
	const totalAmount = items.reduce((accumulator, currentValue) => {
		return accumulator + (currentValue.amount || 0);
	}, 0);
	frm.set_value("total", totalAmount);
	frm.refresh_field("total");
}

function update_total_qty(frm) {
	let items = frm.doc.items || [];
	const totalQty = items.reduce((accumulator, currentValue) => {
		return accumulator + (currentValue.qty || 0);
	}, 0);
	frm.set_value("total_qty", totalQty);
	frm.refresh_field("total_qty");
}

function calc_amount_one_row(frm, cdt, cdn){
	let row = frappe.get_doc(cdt , cdn);
		let qty = row.qty ;
		let rate = row.rate ;
		let amount = qty * rate;
		frappe.model.set_value(cdt , cdn , 'amount' , amount);
}