# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, SUPERUSER_ID, _

class Users(models.Model):
    _inherit = 'res.users'
    #Extend name_get to have the "initials" field in the name
    @api.multi
    def name_get(self):
        result = []
        res = super(res.users, self).name_get()        
        for partner in res:
            initials = ''
            for user in self:
                if user.id == partner.id:
                    initials = user.initials
            if self._context.get('show_initials') and initials != '':
                name = "%s <%s>" % (partner.name, initials)            
            result.append((partner.id, name))
        return result
    #Field to establish the initials of the user
    initials = fields.Char(string="Iniciales")
    
    