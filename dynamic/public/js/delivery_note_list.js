frappe.listview_settings['Delivery Note'] = {

    
    onload: function(listview) {
        listview.page.actions.find('[data-label="%D8%AA%D8%B5%D8%AD%D9%8A%D8%AD"]').parent().parent().remove()  
        listview.page.actions.find(`[data-label="Edit"]`).parent().parent().remove()
        listview.page.actions.find('[data-label="Submit"]').parent().parent().remove()
        listview.page.actions.find('[data-label="%D8%AA%D8%B3%D8%AC%D9%8A%D9%84"]').parent().parent().remove()
        listview.page.actions.find('[data-label="Cancel"]').parent().parent().remove()
        listview.page.actions.find('[data-label="%D8%A5%D9%84%D8%BA%D8%A7%D8%A1"]').parent().parent().remove()
        
    
    }
    
}