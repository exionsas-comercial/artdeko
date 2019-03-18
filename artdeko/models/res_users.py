# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class Users(models.Model):
    _inherit = 'res.users'
    
    #Field to establish the initials of the user
    initials = fields.Char(string="Iniciales")
    #Flag to indicate if user is specifier
    specifier_ok = fields.Boolean('Es especificador', default=False,help="Indica si el usuario es especificador.")
    