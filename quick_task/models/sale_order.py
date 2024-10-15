# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo import Command

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('partner_id.is_only_ordered')
    def if_boolean(self):
        print("hyyy")
        if self.partner_id.is_only_ordered is True:
            filtered_product_line =self.env['sale.order.line'].search([])
            products = self.env['product.template'].search(('invoice_policy', '!=', 'delivery'))
            print("product",products)
            filtered_product_line.product_id = products
            self.create_invoice()
            # if self.partner_id.is_only_ordered is True:
            #     domain = [('invoice_policy', '!=', 'delivery')]
            # else:
            #     domain = []
            # return {'domain': {'line_product_id': {('products': domain)]}}

    def create_invoice(self):
        """create invoice for ordered quntity"""
        for partner in self:
            self.env['account.move'].create([{
                'move_type': 'out_invoice',
                'partner_id': self.partner_id.id,
                'invoice_line_ids': [Command.create({
                    'product_id': self.product_id.id,
                })]
            }])
            template = self.env.ref('quick_task.email_template_invoice_post')
            template.send_mail(partner.id, force_send=True)
