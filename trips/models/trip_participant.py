from odoo import fields, models

class TripParticipant(models.Model):
    _name = "trip.participant"
    _description = "Trip Participant"
    _rec_name = "participant_name"

    trip_id = fields.Many2one('trip')
    participant_age = fields.Char(string='Participant Age')
    participant_name = fields.Char(string='Participant Name', required=True)
    participant_contact = fields.Char(string='Participant Contact', required=True)
    participant_address = fields.Text(string='Participant Address')
    
    doc_type = fields.Selection([
        ('passport', 'Passport'),
        ('id_card', 'ID Card'),
        ('other', 'Other'),
    ], string='Document Type')
    doc_id = fields.Char(string='Document ID')
    attach_file = fields.Binary(string='Attach File')
    expiry_date = fields.Date(string='Expiry Date')

    participant_email = fields.Char(string='Email')
    emergency_contact = fields.Char(string='Emergency Contact', required=True)
