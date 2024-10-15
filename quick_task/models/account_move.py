# -*- coding: utf-8 -*-
from odoo import fields, models, _


class AccountMove(models.Model):
    _inherit = "account.move"

    def action_post(self):
        res = super(AccountMove, self).action_post()
        for record in self:
            if record.move_type in ['out_invoice'] and record.state == 'posted':
                template = self.env.ref('quick_task.email_template_invoice_post')
                template.send_mail(record.partner_id.id, force_send=True)
        return res
