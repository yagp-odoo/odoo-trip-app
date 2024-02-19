{
    'name': "Trips",
    'version': "0.1",
    'depends': ["base"],
    'author': "Yagnik (yagp)",
    'category': "Localization",
    'summary': "Organize and Manage All Your Travels with Odoo Trips",
    'data': [
        "security/ir.model.access.csv",
        "views/trips_records.xml",
        "views/trips_menus.xml",

    ],
    'license': "LGPL-3",
    'installable': True,
    'application': True,
    'auto_install': False,
    'description': """
        Odoo Trips
        ===============
        Organize and Manage Your All Travels With Odoo Trips!!
        Easy to Use!
        Nice UI!
        Accurate Caclulations!
        Expense Tracking!
        Participants, organizers and much more!! """,
}
