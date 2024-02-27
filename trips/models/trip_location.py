from odoo import fields,models

class TripLocation(models.Model):
    _name = "trip.location"
    _description = "Trip Loactions"
    _rec_name = "location_name"

    location_name = fields.Char(string="Location Name")
    location_id = fields.Char(string="Location ID", required=True)
    cost_per_day = fields.Integer(string="Cost per day")
    address = fields.Text(string="Location Address")
    loc_website = fields.Char(string="Location Website")
    loc_temperature = fields.Integer(string="Temperature")
    loc_conditions = fields.Selection(
        selection=[
            ('prime','Prime'),
            ('sunny','Sunny'),
            ('rainy','Rainy'),
        ],
        string="Location Condition"
        )
    loc_description = fields.Text(string="Location Description")
