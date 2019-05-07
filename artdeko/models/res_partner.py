# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class Partner(models.Model):
    _inherit = 'res.partner'
    #Extend name_get to have the "initials" field in the name
    @api.multi
    def name_get(self):
        result = []
        res = super(Partner, self).name_get()        
        for partner in res:
            partner_id, name = partner
            initials = ''
            users = self.env['res.users'].search([('partner_id', '=', partner_id)])
            for user in users:                
                initials = user.initials
            if self._context.get('show_initials') and initials != '':
                name = "%s <%s>" % (name, initials)            
            result.append((partner_id, name))
        return result
    #Hacer obligatorios los campos de email, teléfono y ciudad para los clientes
    phone = fields.Char(required=True)