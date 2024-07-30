data = {

    'custom_fields': {


        "Mode of Payment":[
            {
                "fieldname":"deduction_secion",
                "insert_after":"accounts",
                "fieldtype": "Section Break",
                "label":"Deduction Section"
            },
            {
                "fieldname": "has_deduct",
                "fieldtype": "Check",
                "insert_after": "deduction_secion",
                "label": "Has Deduct"
            },
            {
                "fieldname": "deduct_percentage",
                "fieldtype": "Float",
                "insert_after": "has_deduct",
                "label": "Deduction Percentage",
                "mandatory_depends_on":"eval:doc.has_deduct==1",
                "default":""
            },
            {
                "fieldname":"deduct_column_break",
                "insert_after":"deduct_percentage",
                "fieldtype": "Column Break"
            },
            {
                "fieldname": "recived_account",
                "fieldtype": "Link",
                "insert_after": "deduct_column_break",
                "label": "Recive Account",
                "options":"Account",
                "mandatory_depends_on":"eval:doc.has_deduct==1"
            },
            {
                "fieldname": "cost_center",
                "fieldtype": "Link",
                "insert_after": "deduct_column_break",
                "label": "Cost Center",
                "options":"Cost Center",
                "mandatory_depends_on":"eval:doc.has_deduct==1"
            },
            {
                "fieldname":"naming",
                "fieldtype":"Select",
                "label":"Naming Template",
                "insert_after":"type",
                "options":"\nProjects-.YYYY.-\nHeliopolis-.YYYY.-\nNew Cairo-.YYYY.-\nZayed-.YYYY.-\nMohandseen-.YYYY.-\nMain-.YYYY.-"
            }
        ],
        "Payment Entry":[
            {
                "fieldname":"mode_of_payment_naming",
                "fieldtype":"Data",
                "insert_after":"title",
                "hidden":1,
                "no_copy":1
            }
        ],
    # 'on_setup': 'dynamic.terra.setup.create_payment_deduction_scripts'
    
    }
}