from odoo import api, models


class Lead(models.Model):
    _inherit = 'crm.lead'
    @api.multi
    def action_new_quotation_request(self):
        """
        Request quotation.
        """
        quotation_request = {}        
        quotation_request = {
            'type': 'ir.actions.act_window',
            'res_model': 'mail.activity',
            'view_mode': 'form',
            'view_type': 'form',
            'views': [[False, 'form']],
            'target': 'new',
            'context': {
                'default_activity_type_id': 7,
                'default_res_id': self.id,
                'default_res_model': 'crm.lead',
                'default_summary': 'Solicitud de Cotización',
                'default_note': 'Por favor realizar cotización de esta oportunidad, con los siguientes productos:',
            },
        }        
        return quotation_request
        