from odoo import fields, models

class division(models.Model):
    _name = 'artdeko.division'
    _description = "Division Model"

    name = fields.Char(string="Nombre")