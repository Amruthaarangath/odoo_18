# -*- coding: utf-8 -*-

from odoo import fields, models


class StockPicking(models.Model):
    """Class for inherit stock picking to add fields"""
    _inherit = 'stock.picking'

    return_order = fields.Many2one('sale.return', string='Return order',
                                   help="Shows the return order of current transfer")
    return_order_pick = fields.Many2one('sale.return',
                                        string='Return order Pick',
                                        help="Shows the return order picking  of current return order")
