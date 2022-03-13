from odoo import fields, models

class division(models.Model):
    _name = 'artdeko.division'
    
    name = fields.Char(string="Nombre")