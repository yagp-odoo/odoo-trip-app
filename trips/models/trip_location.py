from odoo import fields, models, api
import requests


ADDRESS_FIELDS = ('street', 'street2', 'zip', 'city', 'state_id', 'country_id')

class TripLocation(models.Model):
    _name = "trip.location"
    _description = "Trip Locations"

    name = fields.Char(string="Location Name")
    location_id = fields.Char(string="Location ID", required=True)
    cost_per_day = fields.Integer(string="Cost Per Day")

    # address fields
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict', domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    country_code = fields.Char(related='country_id.code', string="Country Code")

    loc_website = fields.Char(string="Location Website")
    loc_temperature = fields.Integer(string="Temperature")
    loc_conditions = fields.Selection(
        selection=[
            ('prime', 'Prime'),
            ('sunny', 'Sunny'),
            ('rainy', 'Rainy'),
        ],
        string="Location Condition"
    )
    loc_description = fields.Text(string="Location Description")
    latitude = fields.Float(string="Latitude", compute="_compute_coordinates", store=True, tracking=True)
    longitude = fields.Float(string="Longitude", compute="_compute_coordinates", store=True, tracking=True)

    @api.depends('name', 'city')
    def _compute_map_view_data(self):
        for record in self:
            record.map_view_data = record

    @api.depends('city')
    def _compute_coordinates(self):
        for record in self:
            if record.city:
                latitude, longitude = self._get_coordinates_from_address(record.city)
                record.latitude = latitude
                record.longitude = longitude
            else:
                record.latitude = record.longitude = 0.0

    def _get_coordinates_from_address(self, city):
        url = f"https://nominatim.openstreetmap.org/search?format=json&q={city}"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise exception for HTTP errors
            data = response.json()
            if data:
                latitude = float(data[0]['lat'])
                longitude = float(data[0]['lon'])
                return latitude, longitude
        except Exception as e:
            # Handle exceptions, e.g., log error, return default values, etc.
            pass
        return 0.0, 0.0
