frappe.listview_settings['Stock Entry'] = {

    
    onload: function(listview) {
        
        listview.page.actions.find('[data-label="Edit"]').parent().parent().remove()
        listview.page.actions.find('[data-label="Submit"]').parent().parent().remove()
        listview.page.actions.find('[data-label="Cancel"]').parent().parent().remove()
    }
    
}