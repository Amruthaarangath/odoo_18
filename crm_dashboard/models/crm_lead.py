# -*- coding: utf-8 -*-

from odoo import fields, models, api
import math

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.model
    def get_tiles_data(self):
        """ Return the tile data"""
        company_id = self.env.company
        leads = self.search([('company_id', '=', company_id.id),
                             ('user_id', '=', self.env.user.id)])
        lost_leads= self.search([('user_id', '=', self.env.user.id),
                             ('active', '=',False)])
        my_leads = leads.filtered(lambda r: r.type == 'lead')
        my_leads_mmm = leads.browse(25)
        my_opportunity = leads.filtered(lambda r: r.type == 'opportunity')
        currency = company_id.currency_id.symbol
        expected_revenue = sum(my_opportunity.mapped('expected_revenue'))
        invoice_count = self.env['sale.order'].search([('state','!=','posted'),('user_id','=',self.env.user.id)])
        revenue_total = sum(invoice_count.mapped('amount_total'))
        won_leads = leads.filtered(lambda r: r.stage_id.id == 4)
        ratio = math.gcd(len(lost_leads),len(won_leads))
        lead_ratio = []
        if (len(lost_leads) > 0 ) and (len(won_leads) > 0):
            lead_ratio.append(len(lost_leads)/ratio)
            lead_ratio.append(len(won_leads)/ratio)
        else:
            lead_ratio.append(len(lost_leads))
            lead_ratio.append(len(won_leads))


        # print("won_leads",leads_activity)
        return {
            'total_leads': len(my_leads),
            'total_opportunity': len(my_opportunity),
            'expected_revenue': expected_revenue,
            'currency': currency,
            'revenue_total': revenue_total,
            'lead_ratio' : lead_ratio,
        }

    @api.model
    def get_bar_data(self):
        """Return Lost oppourtunity/lead data for bar chart"""
        lost_leads = self.search([('active', '=', False)])
        leads = lost_leads.filtered(lambda r: r.type == 'lead')
        opportunity = lost_leads.filtered(lambda r: r.type == 'opportunity')
        leads_len = len(leads)
        opportunity_len = len(opportunity)
        print("leads",leads_len)
        print("opportunity",opportunity_len)

        return {
            'leads': len(leads),
            'opportunity': len(opportunity),
        }

    @api.model
    def get_doughnut_data(self):
        """Return Medium data for doughnut chart"""
        medium = self.env['utm.medium'].search([])
        available_medium = []
        for i in medium:
            available_medium.append(i.name)
            print("iii", available_medium)

    @api.model
    def get_line_data(self):
        """ Return campaign data for line chart"""
        campaign = self.env['utm.campaign'].search([])
        print("campaign", campaign)
        available_campaign = []
        for i in campaign:
            available_campaign.append(i.name)
            print("iii", available_campaign)

    @api.model
    def get_pie_data(self):
        activity = self.env["mail.activity.type"].search([])
        activity_list = []
        for i in activity:
            activity_list.append(i.name)
            # print("iii", available_campaign)
        print("activity", activity_list)





