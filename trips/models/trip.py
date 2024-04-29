from odoo import api, exceptions, fields, models
from odoo.tools import html_keep_url, is_html_empty
from odoo.exceptions import ValidationError

class Trips(models.Model):
    _name = "trip"
    _description = "Organize and Manage All Your Travels with Odoo Trips"
    _rec_name = "trip_name"

    accident = fields.Boolean(string='Accident')
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                string="Company",
                                default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency", related='company_id.currency_id')
    details = fields.Text(string='Trip Details')
    end_date = fields.Date(string='End Date')
    expenditure = fields.Monetary(string='Expenditure', compute='_compute_expenditure')
    expected_budget = fields.Monetary(string='Allowed Budget', compute='_compute_expected_budget')
    expenses_ids = fields.One2many('trip.expense' , 'trip_id')
    expense_count = fields.Integer(compute='_compute_offer_count')
    from_location_id = fields.Many2one('trip.location',string='From', help="Trip starting Location")
    loc_cond = fields.Selection(related='to_location_id.loc_conditions', string="Weather Condition", readonly=False)
    loc_temp = fields.Integer(related='to_location_id.loc_temperature')
    location_id = fields.Many2one('trip.location')
    location_ids = fields.One2many('trip.location.entry', 'trips_id', string='Locations', help="Locations Includes in your Trip")
    note = fields.Html(string="Terms and conditions",store=True,readonly=False)
    organizer_budget = fields.Monetary(related='organizer_id.allocated_budget')
    organizer_id = fields.Many2one('organizer', string='Organizer')
    organizer_mail = fields.Char(related='organizer_id.organizer_email')
    participants = fields.One2many('trip.participant.entry', 'trips_id', string='Participants')
    start_date = fields.Date(string='Start Date')
    status = fields.Selection(
        selection=[
            ('draft','Draft'),
            ('planned', 'Planned'),
            ('ongoing', 'Ongoing'),
            ('completed', 'Completed'),
            ('canceled', 'Canceled'),
        ],
        string='Status',
        default='draft',
        store=True,
        compute='_compute_status',
        required=True
        )
    tags_ids = fields.Many2many('trip.tags', string="Tags")
    total_amount = fields.Integer(compute="_compute_total_amount", string="Total Stay Cost", readonly=True, store=True)
    to_location_id = fields.Many2one('trip.location',string='To', help="Trip ending Location")
    travel_days = fields.Integer(compute='_compute_travel_days', string='Travel Days', store=True)
    trip_id = fields.Char(string='Trip ID', copy=False, readonly=True, index=True)
    trip_name = fields.Char(string='Trip Name', required=True)
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

    @api.depends('expenses_ids.amount')
    def _compute_expenditure(self):
        for trip in self:
            trip.expenditure = sum(expense.amount for expense in trip.expenses_ids) + trip.total_amount

    @api.depends('expenses_ids')
    def _compute_offer_count(self):
        for record in self:
            record.expense_count = len(record.expenses_ids)

    @api.depends('organizer_id')
    def _compute_expected_budget(self):
        for trip in self:
            trip.expected_budget = trip.organizer_budget

    @api.depends('start_date', 'end_date')
    def _compute_status(self):
        for trip in self:
            if trip.status == 'planned' and fields.Date.today() >= trip.start_date:
                trip.status = 'ongoing'
            if trip.status == 'ongoing' and fields.Date.today() > trip.end_date:
                trip.status = 'completed'

    @api.depends('location_ids.loc_days', 'location_ids.loc_cost')
    def _compute_total_amount(self):
        for rec in self:
            total_amount = sum(entry.loc_days * entry.loc_cost for entry in rec.location_ids)
            rec.total_amount = total_amount

    @api.depends('start_date', 'end_date')
    def _compute_travel_days(self):
        for record in self:
            if record.start_date and record.end_date:
                delta = record.end_date - record.start_date
                record.travel_days = delta.days
            else:
                record.travel_days = 0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            sequence_value = self.env['ir.sequence'].next_by_code('trip.trip_id')
            vals['trip_id'] = sequence_value
            return super(Trips, self).create(vals)

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

    def open_trip_expense_wizard(self):
        return {
            'name': 'Add Expense',
            'type': 'ir.actions.act_window',
            'res_model': 'add.expense.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('trips.view_trip_expense_wizard_form').id,
            'target': 'new',
            'context': {'default_trip_id': self.id},
        }

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
