from odoo import api, fields, models

class Partner(models.Model):
    _inherit = 'res.partner'
    #Extend name_get to have the "initials" field in the name
    def name_get(self):
        result = []
        res = super().name_get()        
        for partner in res:
            partner_id, name = partner
            initials = ''
            user = self.env['res.users'].search([('partner_id', '=', partner_id)], limit=1)
            initials = user.initials    
            if self._context.get('show_initials') and initials != '':
                name = "%s <%s>" % (name, initials)            
            result.append((partner_id, name))
        return result
