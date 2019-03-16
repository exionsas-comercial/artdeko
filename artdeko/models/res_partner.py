# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.tools.misc import formatLang
from odoo.addons import decimal_precision as dp

class Partner(models.Model):
    _inherit = 'res.partner'
    
    #Field to establish the initials of the user
    initials1 = fields.Char(string="Iniciales")