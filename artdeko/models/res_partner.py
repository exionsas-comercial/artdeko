# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, SUPERUSER_ID, _

class Partner(models.Model):
    _inherit = 'res.partner'
    
    #Field to establish the initials of the user
    initials = fields.Char(string="Iniciales")