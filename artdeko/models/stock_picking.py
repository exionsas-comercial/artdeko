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
    
    #Conectar picking con sale order
    sale_order = fields.Many2one('sale.order', 'Venta')
    #Número de guía del pedido
    guide_number = fields.Char(string='Número de guía')
    #Fecha de salida del pedido desde el proveedor
    departure_date = fields.Datetime('Fecha salida proveedor')
    #Fecha estimada de entrega del proveedor
    estimated_delivery_date = fields.Datetime('Fecha estimada de entrega')
    #Fecha real de entrega del proveedor
    delivery_date = fields.Datetime('Fecha real de entrega')
    #Costos de envío
    shipping_cost = fields.Monetary(string='Costo de envío')