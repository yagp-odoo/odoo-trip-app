from odoo import fields,models

class TripLocationEntry(models.Model):
    _name = "trip.participant.entry"
    _description="Trip Location Entry"

    trips_id = fields.Many2one('trip')
    participant_id = fields.Many2one('trip.participant', required=True)
