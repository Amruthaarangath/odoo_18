#-*- coding: utf-8 -*-

from odoo import _, fields, models, api

class SaleOrder(models.Model):

    _inherit = 'sale.order'

    state = fields.Selection(
        selection_add=[('to_approve', 'To Approve'),('second_approval','Second Approval')]
    )
    first_user = fields.Char(compute = "_compute_partner_approval")
    second_user = fields.Char(compute = "_compute_partner_approval")

    def _compute_partner_approval(self):
        first_approver = self.env['ir.config_parameter'].sudo().get_param('spotter_sale_order_approval.first_user_ids') or False
        second_approver = self.env['ir.config_parameter'].sudo().get_param('spotter_sale_order_approval.second_user_ids') or False
        user = str(self.env.user.id)

        if user in first_approver:
            self.first_user = '1'
        else:
            self.first_user = '0'
        if user in second_approver:
            self.second_user = '1'
        else:
            self.second_user = '0'

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for record in self:
            if record.state == "draft" or record.amount_total >= 25000:
                record.state = "to_approve"
        return res

    def approve_button(self):
        self.state = "second_approval"

    def second_approval_button(self):
        self.state = "sale"
