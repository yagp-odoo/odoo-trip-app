from odoo import fields,models,api

class TripLocationEntry(models.Model):
    _name = "trip.location.entry"
    _description="Trip Location Entry"


    trips_id = fields.Many2one('trip')
    location_id = fields.Many2one('trip.location', required=True)
    loc_cost = fields.Integer(compute="_compute_loc_cost", string="Cost Per Day", readonly=False)
    loc_days = fields.Integer(string="Staying Days")

    @api.depends('location_id')
    def _compute_loc_cost(self):
        for rec in self:
            rec.loc_cost = rec.location_id.cost_per_day
