{
    'name': "Trips",
    'version': "0.1",
    'depends': ["base"],
    'author': "Yagnik (yagp)",
    'category': "Localization",
    'sequence': '-1',
    'summary': "Organize and Manage All Your Travels with Odoo Trips",
    'data': [
        "security/ir.model.access.csv",
        "data/sequences_init.xml",
        "views/trips_records.xml",
        "views/trips_menus.xml",
        "views/trips_views.xml",
        "views/trip_location_views.xml",
        "views/trip_location_entry_views.xml",
        "views/organizer_views.xml",
        "views/trip_participant_views.xml",
        "views/trip_participant_entry_views.xml",
        "views/expense_views.xml",
        "wizard/add_expense_views.xml",

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
