# -*- coding: utf-8 -*-

from odoo import fields, models

class CrmTeam(models.Model):
    _inherit = 'crm.team'

    state_id = fields.Many2one('crm.lead', string = "Stages")
    # lead_state_id = fields.Char(related='state_id.stage_id', string='Payment Field')
