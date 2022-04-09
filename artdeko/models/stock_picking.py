from odoo import api, fields, models


class Picking(models.Model):
    _inherit = 'stock.picking' 
    
    @api.model
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
    #Costos de envío
    shipping_cost = fields.Float('Costo de envío', digits = 'Costo', default=0.0)
    shipping_cost_currency_id = fields.Many2one("res.currency", string="Moneda")
