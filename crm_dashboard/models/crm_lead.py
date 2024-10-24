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
        company_id = self.env.company
        leads = self.search([('company_id', '=', company_id.id),
                             ('user_id', '=', self.env.user.id)])
        leads_medium = []
        medium_name = []
        for i in leads.medium_id:
            new_lead = leads.filtered(lambda r: r.medium_id == i)
            leads_medium.append(len(new_lead))

        for i in leads.medium_id:
            medium_name.append(i.name)

        print("new_lead", leads_medium)
        print("new_lead", medium_name)

        return {
            'leads_medium': leads_medium,
            'medium_name': medium_name,
        }


    @api.model
    def get_line_data(self):
        """ Return campaign data for line chart"""
        company_id = self.env.company
        leads = self.search([('company_id', '=', company_id.id),
                             ('user_id', '=', self.env.user.id)])
        leads_campaign = []
        campaign_name = []
        for i in leads.campaign_id:
            camp_lead = leads.filtered(lambda r: r.campaign_id == i)
            leads_campaign.append(len(camp_lead))

        for i in leads.campaign_id:
            campaign_name.append(i.name)

        print("new_lead", leads_campaign)
        print("new_lead", campaign_name)

        return {
            'leads_campaign': leads_campaign,
            'campaign_name': campaign_name,
        }

    @api.model
    def get_pie_data(self):
        company_id = self.env.company
        leads = self.search([('company_id', '=', company_id.id),
                             ('user_id', '=', self.env.user.id)])
        leads_activity = []
        activity_name = []
        for i in leads.activity_type_id:
            activity_lead = leads.filtered(lambda r: r.activity_type_id == i)
            leads_activity.append(len(activity_lead))

        for i in leads.activity_type_id:
            activity_name.append(i.name)

        print("new_lead", leads_activity)
        print("new_lead", activity_name)

        return {
            'leads_activity': leads_activity,
            'activity_name': activity_name,
        }
    @api.model
    def get_table_data(self):
        company_id = self.env.company
        leads = self.search([('company_id', '=', company_id.id),
                             ('user_id', '=', self.env.user.id)])
        month = [1, "January", 2, 'February',
                 3, 'March',
                 4, 'April',
                 5, 'May',
                 6, 'June',
                 7, 'July',
                 8, 'August',
                 9, 'September',
                 10, 'October',
                 11, 'November',
                 12, 'December']
        leads_medium = []
        month_name = []
        for i in leads:
            new_month_lead = leads.filtered(lambda r: r.create_date.month == i.create_date.month)
            leads_medium.append((new_month_lead))

        for i in leads_medium:
            for j in i:
                month_name.append(j.create_date.month)

        return {
            'month': dict.fromkeys(month),
            'month_name': dict.fromkeys(month_name),
        }

