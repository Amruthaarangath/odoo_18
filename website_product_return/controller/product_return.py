# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import http
from odoo.http import request


class CustomerRegistration(http.Controller):

    @http.route('/sale_return', type='http', methods=['POST'], auth="public", website=True,
                csrf=False)
    def sale_return(self, **kwargs):
        """Controller to create return order"""
        product_id = request.env['product.product'].sudo().browse(int(kwargs['product']))
        order = request.env['sale.order'].sudo().browse(int(kwargs['order_id']))
        qty = kwargs['qty']
        reason = kwargs['reason']
        values = {
            'partner_id': order.partner_id.id,
            'sale_order': order.id,
            'product_id': product_id.id,
            'quantity': qty,
            'reason': reason,
            'user_id': request.env.uid,
            'create_date': datetime.now(),
        }
        stock_picks = request.env['stock.picking'].search([('origin', '=', order.name)])
        moves = stock_picks.mapped('move_ids_without_package').with_user(1).filtered(lambda p: p.product_id == product_id)
        if moves:
            moves = moves.sorted('product_uom_qty', reverse=True)
            values.update({'state': 'draft'})
            ret_order = request.env['sale.return'].with_user(1).create(values)
            moves[0].picking_id.return_order = ret_order.id
            moves[0].picking_id.return_order_picking = False
        return request.redirect('/my/request-thank-you')

    @http.route('/my/request-thank-you', website=True, page=True, auth='public', csrf=False)
    def maintenance_request_thanks(self):
        return request.render('website_return_management.customers_request_thank_page')

