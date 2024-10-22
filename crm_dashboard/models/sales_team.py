# -*- coding: utf-8 -*-

from odoo import fields, models

class CrmTeam(models.Model):
    _inherit = 'crm.team'

    state_id = fields.Many2one('crm.stage', string = "Stages", store=True)
