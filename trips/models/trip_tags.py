from odoo import models,fields

class TripTags(models.Model):
    _name = "trip.tags"
    _description = "Trips Tags"
    _rec_name = "tag"
    _order = "tag"

    tag = fields.Char(required=True, string="Trips Tag")
    color = fields.Integer()

    # SQL Contraint for Unique Trips Tags
    _sql_constraints = [
        ('tag_uniq', "unique(tag)", 
         "Trips Tag Must Not Be Same!")
    ]
