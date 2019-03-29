# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.tools.misc import formatLang
from odoo.addons import decimal_precision as dp

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
    #Fecha real de entrega del proveedor
    delivery_date = fields.Datetime('Fecha real de entrega')
    #Costos de envío
    shipping_cost = fields.Float('Costo de envío', digits=dp.get_precision('Costo'), default=0.0)