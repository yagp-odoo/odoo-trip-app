from odoo import fields,models

class Organizer(models.Model):
    _name = "organizer"
    _description = "Organizers"
    
    organizer_name = fields.Char(string="Organizer Name")
    organizer_email = fields.Char(string="Organizer Email")
    allocated_budget = fields.Float(string="Allocated Budget")