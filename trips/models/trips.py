from odoo import models,fields

class Trips(models.Model):
    _name = "trips"
    _description = "Organize and Manage All Your Travels with Odoo Trips"
    _rec_name = "trip_name"

    trip_id = fields.Char(string='Trip ID', copy=False, readonly=True, index=True, default=lambda self: self.env['ir.sequence'].next_by_code('your.module.trip_sequence'))
    trip_name = fields.Char(string='Trip Name', required=True)
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    organizer_id = fields.Many2one('res.partner', string='Organizer')
    location_id = fields.Char(string='Location (Many2one)')
    details = fields.Text(string='Trip Details')
    from_location_id = fields.Char(string='From (Many2one)')
    to_location_id = fields.Char(string='To (Many2one)')
    status = fields.Selection([
        ('planned', 'Planned'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ], string='Status', default='planned')
    accident = fields.Boolean(string='Accident')
    trip_type = fields.Selection([
        ('business', 'Business'),
        ('vacation', 'Vacation'),
        ('other', 'Other'),
    ], string='Trip Type')
    travel_mode = fields.Selection([
        ('car', 'Car'),
        ('plane', 'Plane'),
        ('train', 'Train'),
        ('other', 'Other'),
    ], string='Travel Mode')
    budget = fields.Float(string='Budget')
