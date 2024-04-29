from odoo import models, fields, api

class TripExpense(models.Model):
    _name = 'trip.expense'
    _description = 'Trip Expense'

    name = fields.Char(string='Expense Name', required=True)
    date = fields.Date(string='Expense Date', required=True)
    expense_category = fields.Many2one('trip.expense.category', string="Category", required=True)
    amount = fields.Float(string='Amount', required=True)
    description = fields.Text(string='Description')
    trip_id = fields.Many2one('trip', string='Trip')
