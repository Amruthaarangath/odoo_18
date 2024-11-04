# -*- coding: utf-8 -*-

from odoo import fields, models, api


class StockReturnPicking(models.TransientModel):
    """Class for inherit stock return picking"""
    _inherit = 'stock.return.picking'

    def _create_returns(self):
        """Function for creating stock return"""
        new_picking, pick_type_id = super(StockReturnPicking,
                                          self)._create_returns()
        picking = self.env['stock.picking'].browse(new_picking)
        if self.picking_id.return_order:
            picking.write({'return_order_picking': False,
                           'return_order': False,
                           'return_order_pick': self.picking_id.return_order.id})
            self.picking_id.return_order.write({'state': 'confirm'})
        return new_picking, pick_type_id

class StockPicking(models.Model):
    """Class for inherit stock picking to add fields"""
    _inherit = 'stock.picking'

    return_order = fields.Many2one('sale.return', string='Return order',
                                   help="Shows the return order of current transfer")
    return_order_pick = fields.Many2one('sale.return',
                                        string='Return order Pick',
                                        help="Shows the return order picking  of current return order")
    return_order_picking = fields.Boolean(string='Return order picking',
                                          help="Helps to identify delivery and return picking, if true the transfer is return picking else delivery")

    def button_validate(self):
        """Function for validate stock picking"""
        res = super(StockPicking, self).button_validate()
        for rec in self:
            if rec.return_order_pick:
                if any(line.state != 'done' for line in
                       rec.return_order_pick.stock_picking):
                    return res
                else:
                    rec.return_order_pick.write({'state': 'done'})
        return res