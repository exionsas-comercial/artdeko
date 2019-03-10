# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _

class division(models.Model):
    _name = 'artdeko.division'
    name = fields.Char(string="Nombre")