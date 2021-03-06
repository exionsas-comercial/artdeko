# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.tools.misc import formatLang
from odoo.addons import decimal_precision as dp

class SaleOrder(models.Model):
    _inherit = 'sale.order'    
    
    @api.multi
    def sale_amount_to_text(self):
        """Method to transform a float amount to text words
        E.g. 100 - ONE HUNDRED
        :returns: Amount transformed to words mexican format for invoices
        :rtype: str
        """
        self.ensure_one()
        currency = self.currency_id.name.upper()
        # M.N. = Moneda Nacional (National Currency)
        # M.E. = Moneda Extranjera (Foreign Currency)
        currency_type = 'M.N' if currency == 'MXN' else 'M.E.'
        # Split integer and decimal part
        amount_i, amount_d = divmod(self.amount_total, 1)
        amount_d = round(amount_d, 2)
        amount_d = int(round(amount_d * 100, 2))
        words = self.currency_id.with_context(lang=self.partner_id.lang or 'es_ES').amount_to_text(amount_i).upper()
        sale_order_words = '%(words)s %(amount_d)02d/100 %(curr_t)s' % dict(
            words=words, amount_d=amount_d, curr_t=currency_type)
        return sale_order_words
    
    @api.multi
    def prepare_purchase_lines_from_sale_order(self):
        """
        Prepare the dict of values to create the new purchase line from sales order line.
        """
        purchase_lines = {}        
        purchase_lines = {
            'name': 'Orden de compra',
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order',
            'view_mode': 'form,tree,graph',            
        }
        self.ensure_one()       
        line3 = []
        for line in self.order_line:
            # Reset date, price and quantity since _onchange_quantity will provide default values
            date_planned = datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
            price_unit = 0.0
            product_uom = line.product_id.uom_po_id or line.product_id.uom_id
                        
            line1 = {'product_id': line.product_id.id,'name': line.name,'product_uom': product_uom.id,'date_planned': date_planned,'price_unit': price_unit,'product_qty': line.product_uom_qty,}            
            line2 = (0,0,line1)
            line3.append(line2)        
        purchase_lines['context'] = {'default_order_line': line3,'default_sale_order':self.id,}
        return purchase_lines
    
    @api.multi    
    def action_new_purchase_request(self):
        """
        Request purchase.
        """
        purchase_request = {}        
        purchase_request = {
            'type': 'ir.actions.act_window',
            'res_model': 'mail.activity',
            'view_mode': 'form',
            'view_type': 'form',
            'views': [[False, 'form']],
            'target': 'new',
            'context': {
                'default_activity_type_id': 6,
                'default_res_id': self.id,
                'default_res_model': 'sale.order',
                'default_summary': 'Solicitud de Orden de Compra',
                'default_note': 'Por favor realizar la compra de los productos de la presente cotización',
            },
        }        
        return purchase_request
    
    @api.multi
    def action_invoice_request(self):
        """
        Request purchase.
        """
        invoice_request = {}        
        invoice_request = {
            'type': 'ir.actions.act_window',
            'res_model': 'mail.activity',
            'view_mode': 'form',
            'view_type': 'form',
            'views': [[False, 'form']],
            'target': 'new',
            'context': {
                'default_activity_type_id': 10,
                'default_res_id': self.id,
                'default_res_model': 'sale.order',
                'default_summary': 'Solicitud de Factura',
                'default_note': 'Por favor realizar la factura de la presente cotización',
            },
        }        
        return invoice_request
    
    @api.multi
    def action_view_purchases(self):
        '''
        Return the view of the sale order´s purchases.
        Can be the tree view if the list have mores than one items, or
        the form view if there is only one purchase.        
        '''
        self.ensure_one()        
        action = self.env.ref('artdeko.sale_purchase_orders_tree').read()[0]        
        purchases = self.env['purchase.order'].search([('sale_order', '=', self.id)])
        if len(purchases) > 1:
            action['domain'] = [('id', 'in', purchases.ids)]        
        elif purchases:
            action['views'] = [(self.env.ref('purchase.purchase_order_form').id, 'form')]
            action['res_id'] = purchases.id        
        return action
    
    @api.multi
    def action_view_receipt(self):
        '''
        Return the view of the pickings asociate with the sale order´s purchases.
        Can be the tree view if the list have mores than one items, or
        the form view if there is only one picking.        
        '''
        action = self.env.ref('stock.action_picking_tree_all').read()[0]        
        action['context'] = {}
        purchases = self.env['purchase.order'].search([('sale_order', '=', self.id)])
        pick_ids = purchases.mapped('picking_ids')        
        if not pick_ids or len(pick_ids) > 1:
            action['domain'] = "[('id','in',%s)]" % (pick_ids.ids)
        elif len(pick_ids) == 1:
            res = self.env.ref('stock.view_picking_form', False)
            action['views'] = [(res and res.id or False, 'form')]
            action['res_id'] = pick_ids.id
        return action
    
    @api.multi
    def _compute_purchase_ids(self):
        '''
        Calculate the quantity of the purchases for each sale order and update the data base.
        '''
        purchases_names = ""
        for order in self:
            purchases = self.env['purchase.order'].search([('sale_order', '=', order.id)])
            order.purchase_count = len(purchases)
            if order.purchase_count == 1:
                purchases_names = self.env['purchase.order'].search([('sale_order', '=', order.id)], limit=1).name
            elif order.purchase_count > 1:                
                for purchase in purchases:
                    purchases_names = purchases_names + purchase.name + ", "
            order.purchase_string = purchases_names
            
    @api.multi
    def _compute_receipt_ids(self):
        '''
        Calculate the quantity of the pickings asociate with the purchases for each sale order and update the data base.
        '''
        for order in self:
            receipts = self.env['purchase.order'].search_read([('sale_order', '=', order.id)], ['picking_count'])
            order.receipt_count = sum([item['picking_count'] for item in receipts])
            
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
    