from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'    
              
    #Campo para asociar las divisiones
    division = fields.Many2one('artdeko.division', string="División", null=True)
    #Campo para asociar los canales
    team_id = fields.Many2one('crm.team', string='Canal', null=True)