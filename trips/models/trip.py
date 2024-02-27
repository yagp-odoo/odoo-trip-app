from odoo import models,fields,api,exceptions
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
    location_ids = fields.Char(string='Location (Many2one)', help="Locations Includes in your Trip.")
    details = fields.Text(string='Trip Details')
    from_location_id = fields.Many2one('trip.location',string='From', help="Trip starting Location")
    to_location_id = fields.Many2one('trip.location',string='To', help="Trip ending Location")
    status = fields.Selection(
        selection=[
            ('draft','Draft'),
            ('planned', 'Planned'),
            ('ongoing', 'Ongoing'),
            ('completed', 'Completed'),
            ('canceled', 'Canceled'),
        ], 
        string='Status', default='draft')
    accident = fields.Boolean(string='Accident')
    trip_type = fields.Selection(
        selection=[
            ('business', 'Business'),
            ('vacation', 'Vacation'),
            ('other', 'Other'),
        ], 
        string='Trip Type')
    travel_mode = fields.Selection(
        selection=[
            ('car', 'Car'),
            ('plane', 'Plane'),
            ('train', 'Train'),
            ('other', 'Other'),
        ], 
        string='Travel Mode')
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
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            sequence_value = self.env['ir.sequence'].next_by_code('trip.trip_id')
            vals['trip_id'] = sequence_value
            return super(Trips, self).create(vals)

    def plan_trip(self):
        for trip in self:
            if trip.status == 'canceled':
                raise exceptions.UserError("Canceled Trips Can't Be Planned!")
            elif trip.status == 'draft':
                # Update property state
                trip.status = 'planned'
            else:
                raise exceptions.UserError("Invalid Trip Status for Planning!")
        return True
    
    def cancel_trip(self):
        for trip in self:
            if trip.status == 'ongoing':
                raise exceptions.UserError("Ongoing Trips Can't Be Canceled")
            else:
                trip.status = 'canceled'
        return True
    def complate_trip(self):
        for trip in self:
            if trip.status == 'ongoing':
                trip.status = 'completed'
            else:
                raise exceptions.UserError("Invalid Trip Status for Complate!")
        return True
