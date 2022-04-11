from odoo import api, fields, models

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    # Adicionar campo para descuentos
    amount_discounted = fields.Monetary(string='Descuentos', store=True, readonly=True, compute='_amount_all')
    #Conectar purchase order con sale order
    sale_order = fields.Many2one('sale.order', string='Venta', default=None)

    # Incluir descuentos en los cálculos
    @api.model
    def _amount_all(self):
        super(PurchaseOrder, self)._amount_all()
        for order in self:
            amount_discounted = 0.0
            for line in order.order_line:
                amount_discounted += line.amount_discount_line
            order.update({
                'amount_discounted': order.currency_id.round(amount_discounted),                
            })


    def purchase_amount_to_text(self):
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
        purchase_order_words = '%(words)s %(amount_d)02d/100 %(curr_t)s' % dict(
            words=words, amount_d=amount_d, curr_t=currency_type)
        return purchase_order_words
        

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'    
    # Adicionar campo para descuentos
    discount = fields.Float(string='Descuento (%)', digits='Discount', default=0.0)
    amount_discount_line = fields.Monetary(compute='_compute_amount', string='Importe descuento', store=True)
    
    # Incluir el descuento en los cálculos
    @api.model
    @api.depends('discount')
    def _prepare_compute_all_values(self):
        computed_values = super(PurchaseOrderLine, self)._prepare_compute_all_values()
        amount_discount = (self.discount * self.price_unit)/100
        computed_values['price_unit'] = self.price_unit - amount_discount
        return computed_values

    @api.model
    @api.depends('product_qty', 'price_unit', 'taxes_id', 'discount')
    def _compute_amount(self):
        super(PurchaseOrderLine, self)._compute_amount()
        for line in self:
            amount_discount = (line.discount * line.price_unit)/100
            amount_discount_line = amount_discount * line.product_qty
            taxes = line.taxes_id.compute_all(**line._prepare_compute_all_values())
            line.update({
                'amount_discount_line': amount_discount_line,
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })
                