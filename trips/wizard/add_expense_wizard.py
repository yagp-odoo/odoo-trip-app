from odoo import models, fields, api

class AddExpenseWizard(models.TransientModel):
    _name = 'add.expense.wizard'
    _description = 'Add Expense to Trip'

    name = fields.Char(string='Expense Name', required=True)
    date = fields.Date(string='Expense Date', required=True)
    expense_category = fields.Many2one('trip.expense.category', string="Category", required=True)
    amount = fields.Float(string='Amount', required=True)
    description = fields.Text(string='Description')

    def add_expense_to_trip(self):
        trip_id = self.env.context.get('active_id')
        if trip_id:
            trip = self.env['trip'].browse(trip_id)
            expense_vals = {
                'name': self.name,
                'date': self.date,
                'expense_category': self.expense_category.id,
                'amount': self.amount,
                'description': self.description,
                'trip_id': trip_id,
            }
            trip_expense = self.env['trip.expense'].create(expense_vals)
            return {
                'name': 'Expense Details',
                'type': 'ir.actions.act_window',
                'res_model': 'trip.expense',
                'view_mode': 'form',
                'res_id': trip_expense.id,
                'view_id': self.env.ref('trips.trip_expense_form').id,
                'target': 'current',
            }
