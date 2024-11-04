# -*- coding: utf-8 -*-

from odoo import api, fields, models

class SaleOrder(models.Model):
    """Class for inherit sale order"""
    _inherit = 'sale.order'

    return_order_count = fields.Integer(compute="_compute_returns",
                                        string='Return Orders',
                                        help='Count of return order')

    def _compute_returns(self):
        """Method to compute return count"""
        sale_return_groups = self.env['sale.return'].sudo().read_group(
            domain=[('sale_order', '=', self.ids)],
            fields=['sale_order'], groupby=['sale_order'])
        orders = self.browse()
        for group in sale_return_groups:
            sale_order = self.browse(group['sale_order'][0])
            while sale_order:
                if sale_order in self:
                    sale_order.return_order_count += group['sale_order_count']
                    orders |= sale_order
                    sale_order = False
        (self - orders).return_order_count = 0

    def action_open_returns(self):
        """This function returns an action that displays the sale return orders from sale order"""
        action = self.env['ir.actions.act_window']._for_xml_id(
            'website_product_return.action_sale_return')
        domain = [('sale_order', '=', self.id)]
        action['domain'] = domain
        action['context'] = {'search_default_order': 1}
        return action