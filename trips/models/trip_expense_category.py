from odoo import models, fields

class ExpenseCategory(models.Model):
    _name = 'trip.expense.category'
    _description = 'Expense Category'
    _rec_name = 'expense_category_name'

    expense_category_name = fields.Char(string='Category Name', required=True)
