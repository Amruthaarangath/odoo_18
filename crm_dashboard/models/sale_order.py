# -*- coding: utf-8 -*-

from odoo import fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            if order.opportunity_id:
                lead = order.opportunity_id
                if lead.stage_id != order.team_id.state_id:
                    lead.stage_id = order.team_id.state_id
        return res
