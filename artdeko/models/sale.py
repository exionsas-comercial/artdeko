from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    #Campo para tener el conteo de las ordenes de compra que se han generado por la venta
    purchase_count = fields.Integer(string='Ordenes de compra', compute='_compute_purchase_ids')
    #Campo para tener en un string los códigos de las ordenes de compra que se han generado por la venta
    purchase_string = fields.Char(string='Ordenes de compra', compute='_compute_purchase_ids')
    #Campo para tener el conteo de las recepciones relacionadas con la venta através de las compras
    receipt_count = fields.Integer(string='Recepciones', compute='_compute_receipt_ids')
    #Campo para asociar las divisiones
    division = fields.Many2one('artdeko.division', string="División", null=True)
    #Campo para asociar los canales
    team_id = fields.Many2one('crm.team', string='Canal', oldname='section_id', null=True)
    #Campo para asociar los especificadores
    specifier_id = fields.Many2one('res.users', string='Especificador', index=True, null=True, domain=[('specifier_ok', '=', True)], context={'show_initials': True})
    
    def _compute_purchase_ids(self):
        '''
        Calculate the quantity of the purchases for each sale order and update the data base.
        '''
        purchases_names = ""
        purchases = self.env['purchase.order'].search([('sale_order', '=', self.id)])
        self.purchase_count = len(purchases)
        if self.purchase_count == 1:
            purchases_names = self.env['purchase.order'].search([('sale_order', '=', self.id)], limit=1).name
        elif self.purchase_count > 1:                
            for purchase in purchases:
                purchases_names = purchases_names + purchase.name + ", "
        self.purchase_string = purchases_names
            
    def _compute_receipt_ids(self):
        '''
        Calculate the quantity of the pickings asociate with the purchases for each sale order and update the data base.
        '''
        receipts = self.env['purchase.order'].search_read([('sale_order', '=', self.id)], ['picking_count'])
        self.receipt_count = sum([item['picking_count'] for item in receipts])