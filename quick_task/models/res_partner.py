# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_only_ordered = fields.Boolean(string="Ordered Only")

