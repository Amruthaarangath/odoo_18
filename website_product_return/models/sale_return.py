# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ReturnOrder(models.Model):
    """Class for sale order return"""
    _name = 'sale.return'
    _inherit = ['portal.mixin']
    _rec_name = "name"
    _order = "name"
    _description = "Return Order"


    active = fields.Boolean('Active', default=True, help='Is active or not')
    name = fields.Char(string="Name",
                       help='Name of return order', readonly=True, default=lambda self: _('New'), copy=False)
    product_id = fields.Many2one('product.product', string="Product Variant",
                                 required=True,
                                 help="defines the product variant that need to be returned")
    product_tmpl_id = fields.Many2one('product.template',
                                      related="product_id.product_tmpl_id",
                                      store=True,
                                      string="Product", help='Return Product'
                                      )
    sale_order = fields.Many2one('sale.order', string="Sale Order",
                                 required=True, help='Reference of Sale Order')
    partner_id = fields.Many2one('res.partner', string="Customer",
                                 help='Customer of the return order')

    create_date = fields.Datetime(string="Create Date",
                                  help='Create date of the return')
    quantity = fields.Float(string="Quantity", default=0,
                            help='Return quantity')

    reason = fields.Text("Reason", help='Reason of the return')
    stock_picking = fields.One2many('stock.picking', 'return_order_pick',
                                    domain="[('return_order','=',False)]",
                                    string="Return Picking",
                                    help="Shows the return picking of the corresponding return order")
    state = fields.Selection(
        [('draft', 'Draft'), ('done', 'Done'),
         ('cancel', 'Canceled')],
        string='Status', readonly=True, default='draft',
        help='Status of return order')
    source_pick = fields.One2many('stock.picking', 'return_order',
                                  string="Source Delivery",

                                  help="Shows the delivery orders of the corresponding return order")
    note = fields.Text("Note")
    to_refund = fields.Boolean(string='Update SO/PO Quantity',
                               help='Trigger a decrease of the delivered/received quantity in'
                                    ' the associated Sale Order/Purchase Order')

    @api.model_create_multi
    def create(self, vals_list):
        """ Create a sequence for the returned sale orders """
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sale.return')
        return super().create(vals_list)

    def return_confirm(self):
        """Confirm the sale return"""
        if not self.source_pick:
            stock_picks = self.env['stock.picking'].search(
                [('origin', '=', self.sale_order.name)])
            moves = stock_picks.mapped('move_ids_without_package').filtered(
                lambda p: p.product_id == self.product_id)
        else:
            moves = self.source_pick.mapped(
                'move_ids_without_package').filtered(
                lambda p: p.product_id == self.product_id)
        if moves:
            moves = moves.sorted('product_uom_qty', reverse=True)
            pick = moves[0].picking_id
            vals = {'picking_id': pick.id}
            return_pick_wizard = self.env['stock.return.picking'].create(vals)
            lines = {'product_id': self.product_id.id,
                     "quantity": self.quantity,
                     'wizard_id': return_pick_wizard.id,
                     'move_id': moves[0].id, 'to_refund': self.to_refund}
            self.env['stock.return.picking.line'].create(lines)
            return_pick = list(return_pick_wizard.action_create_returns())
            print("return_pick",return_pick)
            self.write({'state': 'done'})
