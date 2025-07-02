from frappe import _ 


data = {
    'custom_fields': {
        'Purchase Order': [
            {
                "label": _("Has Shipped"),
                "fieldname": "has_shipped",
                "fieldtype": "Check",
                "insert_after": "tax_withholding_category",
                "read_only" : 1
            },
        ],
        'Lead':[      
               {
                "fieldname": "interested_categorys",
                "fieldtype": "Select",
                "options": "\nHSG Bending machine\n3D Printer\nCutter Plotter\nforex sheets\nGrando printer\nHans Laser\nHSG fiberlaser\nindoor power supply\nled modules\nled neon strips\nled neon strips+RGB\nled strips\nled strips (zigzag)\nneon led wire\nrainproof power supply\nstainless steel Letter Coil\nUV\nVacuum Forming Machine\nInks\nHARSLE Press break machine\nIcrelic bending machine\nGalvo head machine\nDouble color\nPrinter\nPrinter 160 CM\nCO2 Welding machine\nPlasma machine\nRouter machine\nRouter machine DIACAM\nWelding machine\nJewelry welding machine\nJewelry welding machine DADO\nLetter bending machine\nLetter bending machine HARFMAK\nLaser CO2 machine\nAll machines\nAdvertising staff\nHARSLE Shearing Machine\nHeat Press Machine 8*1\nUnavilable product\nMoba machine\nAdhesive tape\nPrinter\nCutter Plotter\nMaterials\nMaintainance\nFiber marker machine\nFiber cutting machine\nSpare parts",
                "insert_after": "email_id",
                "label": "Interested category",
            },
           ]
    }
}