from odoo import fields,models

class Organizer(models.Model):
    _name = "organizer"
    _description = "Organizers"
    _rec_name = "organizer_name"

    company_id = fields.Many2one('res.company', store=True, copy=False,
                                string="Company",
                                default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency", related='company_id.currency_id')

    
    organizer_name = fields.Char(string="Organizer Name")
    organizer_email = fields.Char(string="Organizer Email")
    allocated_budget = fields.Monetary(string="Allocated Budget",store=True)