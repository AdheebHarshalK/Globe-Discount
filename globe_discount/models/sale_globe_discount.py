
from odoo import fields, models, api,exceptions


class SaleGlobeDiscount(models.Model):
    _inherit = 'sale.order'

    discount = fields.Integer(string='Discount (%)')
    discount_amount = fields.Monetary(string='Discount Amount', compute='_compute_discount_amount', store=True)
    amount_total = fields.Monetary(string="Total", store=True, compute='_compute_amounts',)



    @api.depends('amount_untaxed', 'discount')
    def _compute_discount_amount(self):
        for order in self:
            if 0 <= order.discount <= 100:
                order.discount_amount = (order.amount_untaxed * order.discount) / 100
            else:
                order.discount_amount = 0

    @api.constrains('discount')
    def _check_discount_validity(self):
        for order in self:
            if not 0 <= order.discount <= 100:
                raise exceptions.UserError("Discount percentage must be between 0 and 100.")

    @api.depends('amount_untaxed', 'discount', 'amount_tax')
    def _compute_amounts(self):
        print(self.amount_total)
        super(SaleGlobeDiscount, self)._compute_amounts()

        for order in self:
            order.amount_total -= order.discount_amount
