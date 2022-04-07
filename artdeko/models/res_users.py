from odoo import fields, models

class Users(models.Model):
    _inherit = 'res.users'
    
    #Field to establish the initials of the user
    initials = fields.Char(string="Iniciales")
    #Flag to indicate if user is specifier
    specifier_ok = fields.Boolean('Es especificador', default=False,help="Indica si el usuario es especificador.")
    