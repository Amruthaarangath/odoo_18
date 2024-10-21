# -*- coding: utf-8 -*-

from odoo import fields, models, api

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.model
    def get_tiles_data(self):
        """ Return the tile data"""
        company_id = self.env.company
        leads = self.search([('company_id', '=', company_id.id),
                             ('user_id', '=', self.env.user.id)])
        my_leads = leads.filtered(lambda r: r.type == 'lead')
        my_opportunity = leads.filtered(lambda r: r.type == 'opportunity')
        currency = company_id.currency_id.symbol
        expected_revenue = sum(my_opportunity.mapped('expected_revenue'))
        invoice_count = self.env['sale.order'].search([('state','!=','posted'),('user_id','=',self.env.user.id)])
        revenue = sum(invoice_count.mapped('amount_total'))

        print("revenue",revenue)
        print("invoice_count",invoice_count)
        return {
            'total_leads': len(my_leads),
            'total_opportunity': len(my_opportunity),
            'expected_revenue': expected_revenue,
            'currency': currency,
            'revenue': revenue,
        }