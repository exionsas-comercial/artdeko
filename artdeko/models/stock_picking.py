# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, SUPERUSER_ID, _

class Picking(models.Model):
    _inherit = 'stock.picking' 
    
    @api.multi
    def picking_force_cancel(self):
        """
        Force the stock picking cancelation
        """        
        for move in self.move_lines:
            # Set the "state" to cancel foreach move
            move.write({'state': 'cancel'})
    
    #Conectar purchase order con sale order
    sale_order = fields.Many2one('sale.order', 'Venta')           