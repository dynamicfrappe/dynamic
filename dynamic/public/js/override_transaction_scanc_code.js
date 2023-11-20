

frappe.provide("erpnext");
erpnext.CustomTransactionController =  erpnext.TransactionController.extend({
   

    refresh: function() {
		console,log("new-extend")
        this._super()
	},
    say_hi:function(){
        console.log('hi**************************')
    }
});