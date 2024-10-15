# -*- coding: utf-8 -*-

from odoo import fields, models, _, api
from ast import literal_eval


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    is_sale_order_approve = fields.Boolean(string='Sale Order Approval',
                                       config_parameter='spotter_sale_order_approval.is_sale_order_approve',
                                       help='check this field to set approvals for sale orders greater than 25K')
    first_user_ids = fields.Many2many('res.users','second_user_approver',
      'first_user', 'approve_id', string="First Approver")

    second_user_ids = fields.Many2many('res.users', string="Second Approver")

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'spotter_sale_order_approval.first_user_ids', self.first_user_ids.ids)
        self.env['ir.config_parameter'].sudo().set_param(
            'spotter_sale_order_approval.second_user_ids', self.second_user_ids.ids)
        return res

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        with_user = self.env['ir.config_parameter'].sudo()
        first_user = with_user.get_param('spotter_sale_order_approval.first_user_ids')
        res.update(first_user_ids=[(6, 0, literal_eval(first_user))
                                     ] if first_user else False, )
        second_user = with_user.get_param('spotter_sale_order_approval.second_user_ids')
        res.update(second_user_ids=[(6, 0, literal_eval(second_user))
                                     ] if second_user else False, )
        return res

