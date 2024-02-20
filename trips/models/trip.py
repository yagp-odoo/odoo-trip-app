from odoo import models,fields,api
from dateutil import relativedelta
from datetime import datetime

class Trips(models.Model):
    _name = "trip"
    _description = "Organize and Manage All Your Travels with Odoo Trips"
    _rec_name = "trip_name"

    trip_id = fields.Char(string='Trip ID', copy=False, readonly=True, index=True)
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
    # tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    travel_days = fields.Integer(compute='_compute_travel_days', string='Travel Days', store=True)

    @api.depends('start_date', 'end_date')
    def _compute_travel_days(self):
        for record in self:
            if record.start_date and record.end_date:
                delta = relativedelta.relativedelta(record.end_date,record.start_date)
                record.travel_days = delta.days
            else:
                record.travel_days = 0
    
    @api.model
    def create(self, vals):
        sequence_value = self.env['ir.sequence'].next_by_code('trip.trip_id')
        vals['trip_id'] = sequence_value
        return super(Trips, self).create(vals)
