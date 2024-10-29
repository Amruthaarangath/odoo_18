# -*- coding: utf-8 -*-

from odoo import fields, models, api
import math
from datetime import date


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.model
    def get_tiles_data(self,filter_value):
        """ Return the tile data"""
        today = date.today()
        current_month = today.month
        current_year = today.year
        current_week = today.isocalendar().week
        first_quater = [1, 2, 3, 4, 5, 6]
        second_quater = [7, 8, 9, 10, 11, 12]
        company_id = self.env.company
        print("tttttttttttttttttttttttt",filter_value)
        leads = self.search([('company_id', '=', company_id.id),
                             ('user_id', '=', self.env.user.id)])
        lost_leads= self.search([('user_id', '=', self.env.user.id),
                             ('active', '=',False)])
        my_leads = leads.filtered(lambda r: r.type == 'lead')
        my_opportunity = leads.filtered(lambda r: r.type == 'opportunity')
        currency = company_id.currency_id.symbol
        expected_revenue = sum(my_opportunity.mapped('expected_revenue'))
        invoice_count = self.env['sale.order'].search([('state','!=','posted'),('user_id','=',self.env.user.id)])
        revenue_total = sum(invoice_count.mapped('amount_total'))
        won_leads = leads.filtered(lambda r: r.stage_id.id == 4)
        ratio = math.gcd(len(lost_leads),len(won_leads))
        lead_lost_ratio = []
        lead_won_ratio = []
        if (len(lost_leads) > 0 ) and (len(won_leads) > 0):
            lead_won_ratio.append(len(lost_leads)/ratio)
            lead_won_ratio.append(len(won_leads)/ratio)
        else:
            lead_won_ratio.append(len(lost_leads))
            lead_won_ratio.append(len(won_leads))


        if filter_value == 'this_year':
            print("hyyyy2223333333333333")
            my_leads = leads.filtered(lambda r: r.type == 'lead' and r.create_date.year == current_year)
            my_opportunity = leads.filtered(lambda r: r.type == 'opportunity' and r.create_date.year == current_year)
            expected_revenue = sum(my_opportunity.mapped('expected_revenue'))
            won_leads = leads.filtered(lambda r: r.stage_id.id == 4 and r.create_date.year == current_year)
            if (len(lost_leads) > 0) and (len(won_leads) > 0):
                lead_won_ratio.append(len(lost_leads) / ratio)
                lead_won_ratio.append(len(won_leads) / ratio)
            else:
                lead_won_ratio.append(len(lost_leads))
                lead_won_ratio.append(len(won_leads))

        if filter_value == 'this_week':
            print("hyyyy11111111111")
            my_leads = leads.filtered(lambda r: r.type == 'lead' and r.create_date.isocalendar().week == current_week)
            my_opportunity = leads.filtered(lambda r: r.type == 'opportunity' and r.create_date.isocalendar().week == current_week)
            expected_revenue = sum(my_opportunity.mapped('expected_revenue'))
            won_leads = leads.filtered(lambda r: r.stage_id.id == 4 and r.create_date.isocalendar().week == current_week)
            if (len(lost_leads) > 0) and (len(won_leads) > 0):
                lead_won_ratio.append(len(lost_leads) / ratio)
                lead_won_ratio.append(len(won_leads) / ratio)
            else:
                lead_won_ratio.append(len(lost_leads))
                lead_won_ratio.append(len(won_leads))

        if filter_value == 'this_month':
            print("hyyyy222")
            my_leads = leads.filtered(lambda r: r.type == 'lead' and r.create_date.month == current_month)
            my_opportunity = leads.filtered(lambda r: r.type == 'opportunity' and r.create_date.month == current_month)
            expected_revenue = sum(my_opportunity.mapped('expected_revenue'))
            won_leads = leads.filtered(lambda r: r.stage_id.id == 4 and r.create_date.month == current_month)
            if (len(lost_leads) > 0) and (len(won_leads) > 0):
                lead_won_ratio.append(len(lost_leads) / ratio)
                lead_won_ratio.append(len(won_leads) / ratio)
            else:
                lead_won_ratio.append(len(lost_leads))
                lead_won_ratio.append(len(won_leads))

        if filter_value == 'this_quater':
            print("hyyyy244444444444444444422")
            if current_month in first_quater:
                my_leads = leads.filtered(lambda r: r.type == 'lead' and r.create_date.month in first_quater)
                my_opportunity = leads.filtered(lambda r: r.type == 'opportunity' and r.create_date.month in first_quater)
                expected_revenue = sum(my_opportunity.mapped('expected_revenue'))
                won_leads = leads.filtered(lambda r: r.stage_id.id == 4 and r.create_date.month in first_quater)
                if (len(lost_leads) > 0) and (len(won_leads) > 0):
                    lead_won_ratio.append(len(lost_leads) / ratio)
                    lead_won_ratio.append(len(won_leads) / ratio)
                else:
                    lead_won_ratio.append(len(lost_leads))
                    lead_won_ratio.append(len(won_leads))
            else:
                my_leads = leads.filtered(lambda r: r.type == 'lead' and r.create_date.month in second_quater)
                my_opportunity = leads.filtered(lambda r: r.type == 'opportunity' and r.create_date.month in second_quater)
                expected_revenue = sum(my_opportunity.mapped('expected_revenue'))
                won_leads = leads.filtered(lambda r: r.stage_id.id == 4 and r.create_date.month in second_quater)
                if (len(lost_leads) > 0) and (len(won_leads) > 0):
                    lead_won_ratio.append(len(lost_leads) / ratio)
                    lead_won_ratio.append(len(won_leads) / ratio)
                else:
                    lead_won_ratio.append(len(lost_leads))
                    lead_won_ratio.append(len(won_leads))




        return {
            'total_leads': len(my_leads),
            'total_opportunity': len(my_opportunity),
            'expected_revenue': expected_revenue,
            'currency': currency,
            'revenue_total': revenue_total,
            'lead_won_ratio' : lead_won_ratio,
        }

    @api.model
    def get_bar_data(self, filter_value):
        """Return Lost oppourtunity/lead data for bar chart"""
        today = date.today()
        current_month = today.month
        current_year = today.year
        current_week = today.isocalendar().week
        first_quater = [1, 2, 3, 4, 5, 6]
        second_quater = [7, 8, 9, 10, 11, 12]
        lost_leads = self.search([('active', '=', False)])
        leads = lost_leads.filtered(lambda r: r.type == 'lead')
        opportunity = lost_leads.filtered(lambda r: r.type == 'opportunity')
        leads_len = len(leads)
        opportunity_len = len(opportunity)

        if filter_value == 'this_year':
            leads = lost_leads.filtered(lambda r: r.type == 'lead' and r.create_date.year == current_year)
            opportunity = lost_leads.filtered(lambda r: r.type == 'opportunity' and r.create_date.year == current_year)

        if filter_value == 'this_week':
            leads = lost_leads.filtered(lambda r: r.type == 'lead' and r.create_date.isocalendar().week == current_week)
            opportunity = lost_leads.filtered(lambda r: r.type == 'opportunity' and r.create_date.isocalendar().week == current_week)

        if filter_value == 'this_month':
            leads = lost_leads.filtered(lambda r: r.type == 'lead' and r.create_date.month == current_month)
            opportunity = lost_leads.filtered(lambda r: r.type == 'opportunity' and r.create_date.month == current_month)

        if filter_value == 'this_quater':
            if current_month in first_quater:
                leads = lost_leads.filtered(lambda r: r.type == 'lead' and r.create_date.month in first_quater)
                print("leads first", leads)
                opportunity = lost_leads.filtered(lambda r: r.type == 'opportunity' and r.create_date.month in first_quater)
            else:
                leads = lost_leads.filtered(lambda r: r.type == 'lead' and r.create_date.month in second_quater)
                print("leads quater", leads)
                opportunity = lost_leads.filtered(
                    lambda r: r.type == 'opportunity' and r.create_date.month in second_quater)

        return {
            'leads': len(leads),
            'opportunity': len(opportunity),
        }

    @api.model
    def get_line_data(self, filter_value):
        """ Return campaign data for line chart"""
        today = date.today()
        current_month = today.month
        current_year = today.year
        current_week = today.isocalendar().week
        first_quater = [1, 2, 3, 4, 5, 6]
        second_quater = [7, 8, 9, 10, 11, 12]
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

        if filter_value == 'this_year':
            for i in leads.campaign_id:
                camp_lead = leads.filtered(lambda r: r.campaign_id == i and r.create_date.year == current_year)
                leads_campaign.append(len(camp_lead))
                campaign_name.append(i.name)

        if filter_value == 'this_week':
            for i in leads.campaign_id:
                camp_lead = leads.filtered(
                    lambda r: r.campaign_id == i and r.create_date.isocalendar().week == current_week)
                leads_campaign.append(len(camp_lead))
                campaign_name.append(i.name)

        if filter_value == 'this_month':
            for i in leads.campaign_id:
                camp_lead = leads.filtered(lambda r: r.campaign_id == i and r.create_date.month == current_month)
                leads_campaign.append(len(camp_lead))
                campaign_name.append(i.name)

        if filter_value == 'this_quater':
            print("yes")
            if current_month in first_quater:
                camp_lead = leads.filtered(
                    lambda r: r.campaign_id == i and r.create_date.month in first_quater)
                leads_campaign.append(len(camp_lead))
                campaign_name.append(i.name)
            else:
                camp_lead = leads.filtered(
                    lambda r: r.campaign_id == i and r.create_date.month in second_quater)
                leads_campaign.append(len(camp_lead))
                campaign_name.append(i.name)

        return {
            'leads_campaign': leads_campaign,
            'campaign_name': campaign_name,
        }


    @api.model
    def get_line_data(self, filter_value):
        """ Return campaign data for line chart"""
        today = date.today()
        current_month = today.month
        current_year = today.year
        current_week = today.isocalendar().week
        first_quater = [1, 2, 3, 4, 5, 6]
        second_quater = [7, 8, 9, 10, 11, 12]
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

        if filter_value == 'this_year':
            for i in leads.campaign_id:
                camp_lead = leads.filtered(lambda r: r.campaign_id == i and r.create_date.year == current_year)
                leads_campaign.append(len(camp_lead))
                campaign_name.append(i.name)

        if filter_value == 'this_week':
            for i in leads.campaign_id:
                camp_lead = leads.filtered(lambda r: r.campaign_id == i and r.create_date.isocalendar().week == current_week)
                leads_campaign.append(len(camp_lead))
                campaign_name.append(i.name)

        if filter_value == 'this_month':
            for i in leads.campaign_id:
                camp_lead = leads.filtered(lambda r: r.campaign_id == i and r.create_date.month == current_month)
                leads_campaign.append(len(camp_lead))
                campaign_name.append(i.name)

        if filter_value == 'this_quater':
            if current_month in first_quater:
                camp_lead = leads.filtered(
                    lambda r: r.campaign_id == i and r.create_date.month in first_quater)
                leads_campaign.append(len(camp_lead))
                campaign_name.append(i.name)
            else:
                camp_lead = leads.filtered(
                    lambda r: r.campaign_id == i and r.create_date.month in second_quater)
                leads_campaign.append(len(camp_lead))
                campaign_name.append(i.name)

        return {
            'leads_campaign': leads_campaign,
            'campaign_name': campaign_name,
        }

    # @api.model
    # def get_doughnut_data(self, filter_value):
    #     """Return Medium data for doughnut chart"""
    #     today = date.today()
    #     current_month = today.month
    #     current_year = today.year
    #     current_week = today.isocalendar().week
    #     first_quater = [1, 2, 3, 4, 5, 6]
    #     second_quater = [7, 8, 9, 10, 11, 12]
    #     company_id = self.env.company
    #     print("filter_valuelkjhgfd", filter_value)
    #     leads = self.search([('company_id', '=', company_id.id),
    #                          ('user_id', '=', self.env.user.id)])
    #     leads_medium = []
    #     medium_name = []
    #     for i in leads.medium_id:
    #         new_lead = leads.filtered(lambda r: r.medium_id == i)
    #         leads_medium.append(len(new_lead))
    #         medium_name.append(i.name)
    #
    #     if filter_value == 'this_year':
    #         for i in leads.medium_id:
    #             new_lead = leads.filtered(lambda r: r.medium_id == i and r.create_date.year == current_year)
    #             leads_medium.append(len(new_lead))
    #             medium_name.append(i.name)
    #
    #     if filter_value == 'this_week':
    #         for i in leads.medium_id:
    #             new_lead = leads.filtered(lambda r: r.medium_id == i and r.create_date.isocalendar().week == current_week)
    #             leads_medium.append(len(new_lead))
    #             medium_name.append(i.name)
    #
    #     if filter_value == 'this_month':
    #         for i in leads.medium_id:
    #             new_lead = leads.filtered(lambda r: r.medium_id == i and r.create_date.month == current_month)
    #             leads_medium.append(len(new_lead))
    #             medium_name.append(i.name)
    #
    #     if filter_value == 'this_quater':
    #         if current_month in first_quater:
    #             for i in leads.medium_id:
    #                 new_lead = leads.filtered(lambda r: r.medium_id == i and r.create_date.month in first_quater)
    #                 leads_medium.append(len(new_lead))
    #                 medium_name.append(i.name)
    #         else:
    #             for i in leads.medium_id:
    #                 new_lead = leads.filtered(lambda r: r.medium_id == i and r.create_date.month in second_quater)
    #                 leads_medium.append(len(new_lead))
    #                 medium_name.append(i.name)
    #
    #
    #
    #     return {
    #         'leads_medium': len(set(leads_medium)),
    #         'medium_name': set(medium_name)
    #     }

    @api.model
    def get_doughnut_data(self, filter_value):
        """Return Medium data for doughnut chart"""
        today = date.today()
        current_month = today.month
        current_year = today.year
        current_week = today.isocalendar().week
        first_quater = [1, 2, 3, 4, 5, 6]
        second_quater = [7, 8, 9, 10, 11, 12]
        company_id = self.env.company
        leads = self.search([('company_id', '=', company_id.id),
                             ('user_id', '=', self.env.user.id)])
        leads_medium = []
        medium_name = []
        for i in leads.medium_id:
            new_lead = leads.filtered(lambda r: r.medium_id == i)
            leads_medium.append(len(new_lead))
            medium_name.append(i.name)

        print("leads_medium", leads_medium)

        if filter_value == 'this_year':
            for i in leads.medium_id:
                new_lead = leads.filtered(lambda r: r.medium_id == i and r.create_date.year == current_year)
                leads_medium.append(len(new_lead))
                medium_name.append(i.name)

        if filter_value == 'this_week':
            for i in leads.medium_id:
                new_lead = leads.filtered(lambda r: r.medium_id == i and r.create_date.isocalendar().week == current_week)
                leads_medium.append(len(new_lead))
                medium_name.append(i.name)

        if filter_value == 'this_month':
            for i in leads.medium_id:
                new_lead = leads.filtered(lambda r: r.medium_id == i and r.create_date.month == current_month)
                leads_medium.append(len(new_lead))
                medium_name.append(i.name)

        if filter_value == 'this_quater':
            if current_month in first_quater:
                for i in leads.medium_id:
                    new_lead = leads.filtered(lambda r: r.medium_id == i and r.create_date.month in first_quater)
                    leads_medium.append(len(new_lead))
                    medium_name.append(i.name)
            else:
                for i in leads.medium_id:
                    new_lead = leads.filtered(lambda r: r.medium_id == i and r.create_date.month in second_quater)
                    leads_medium.append(len(new_lead))
                    medium_name.append(i.name)



        return {
            'leads_medium': leads_medium,
            'medium_name': list(set(medium_name)),
        }

    @api.model
    def get_pie_data(self, filter_value):
        today = date.today()
        current_month = today.month
        current_year = today.year
        current_week = today.isocalendar().week
        first_quater = [1, 2, 3, 4, 5, 6]
        second_quater = [7, 8, 9, 10, 11, 12]
        company_id = self.env.company
        print("filter_valueooooooooooooooooo",filter_value)
        leads = self.search([('company_id', '=', company_id.id),
                             ('user_id', '=', self.env.user.id)])
        leads_activity = []
        activity_name = []
        for i in leads.activity_type_id:
            activity_lead = leads.filtered(lambda r: r.activity_type_id == i)
            leads_activity.append(len(activity_lead))
            activity_name.append(i.name)

        if filter_value == 'this_year':
            for i in leads.activity_type_id:
                activity_lead = leads.filtered(lambda r: r.activity_type_id == i and r.create_date.year == current_year)
                leads_activity.append(len(activity_lead))
                activity_name.append(i.name)

        if filter_value == 'this_week':
            for i in leads.activity_type_id:
                activity_lead = leads.filtered(lambda r: r.activity_type_id == i and r.create_date.isocalendar().week == current_week)
                leads_activity.append(len(activity_lead))
                activity_name.append(i.name)

        if filter_value == 'this_month':
            for i in leads.activity_type_id:
                activity_lead = leads.filtered(lambda r: r.activity_type_id == i and r.create_date.month == current_month)
                leads_activity.append(len(activity_lead))
                activity_name.append(i.name)

        if filter_value == 'this_quater':
            if current_month in first_quater:
                for i in leads.activity_type_id:
                    activity_lead = leads.filtered(lambda r: r.activity_type_id == i and r.create_date.month in first_quater)
                    leads_activity.append(len(activity_lead))
                    activity_name.append(i.name)
            else:
                for i in leads.activity_type_id:
                    activity_lead = leads.filtered(lambda r: r.activity_type_id == i and r.create_date.month in second_quater)
                    leads_activity.append(len(activity_lead))
                    activity_name.append(i.name)

        return {
            'leads_activity': leads_activity,
            'activity_name': activity_name,
        }
    @api.model
    def get_table_data(self, filter_value):
        print("filter_valueiiiiiio",filter_value)
        today = date.today()
        current_month = today.month
        current_year = today.year
        current_week = today.isocalendar().week
        first_quater = [1, 2, 3, 4, 5, 6]
        second_quater = [7, 8, 9, 10, 11, 12]
        company_id = self.env.company
        leads = self.search([('company_id', '=', company_id.id),
                             ('user_id', '=', self.env.user.id)])
        leads_month = []
        leads_month_length = []
        len_leads = []
        name = {1: 'january', 2: 'february', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August',
                9: 'september', 10: 'October', 11: 'November', 12: 'December'}

        for i in leads:
            new_month_lead = leads.filtered(lambda r: r.create_date.month == i.create_date.month)
            leads_month.append((new_month_lead))
            leads_month_length.append(len(new_month_lead))
            monthly_lead = set(leads_month)
            # len_leads.append(len(leads_month))


        month_name = []
        for i in monthly_lead:
            for j in i:
                month_name.append(j.create_date.month)
                months = set(month_name)


        final_month_name = []
        for m in name:
            if m in month_name:
                final_month_name.append(name[m])

        # if filter_value == 'this_year':
        #     for i in leads:
        #         new_month_lead = leads.filtered(lambda r: r.create_date.month == i.create_date.month)
        #         leads_month_length.append(len(new_month_lead))
        #         monthly_lead = set(leads_month)
        #
        #     for m in name:
        #         if m in month_name:
        #             final_month_name.append(name[m])


        return {
            'leads_month_length': list(set(leads_month_length)),
            'final_month_name': final_month_name[::-1]
        }
    #
    @api.model
    def get_filter_data(self, filter_value):
        """filtered data's"""
        today = date.today()
        current_month = today.month
        current_year = today.year
        current_week = today.isocalendar().week
        first_quater = [1,2,3,4,5,6]
        second_quater = [7,8,9,10,11,12]
        company_id = self.env.company

        #bar chart data
        lost_leads = self.search([('active', '=', False)])

        # if filter_value == 'this_month':
        leads = lost_leads.filtered(lambda r: r.type == 'lead' and r.create_date.month == current_month)
        opportunity = lost_leads.filtered(lambda r: r.type == 'opportunity' and r.create_date.month == current_month)
        #
        # if filter_value == 'this_year':
        #     leads = lost_leads.filtered(lambda r: r.type == 'lead' and r.create_date.year == current_year)
        #     print("leads year", leads)
        #     opportunity = lost_leads.filtered(lambda r: r.type == 'opportunity' and r.create_date.year == current_year)
        #
        # if filter_value == 'this_week':
        #     leads = lost_leads.filtered(lambda r: r.type == 'lead' and r.create_date.isocalendar().week == current_week)
        #     print("leads week", leads)
        #     opportunity = lost_leads.filtered(lambda r: r.type == 'opportunity' and r.create_date.isocalendar().week == current_week)
        #
        # if filter_value == 'all':
        #     leads = lost_leads.filtered(lambda r: r.type == 'lead')
        #     print("leads week", leads)
        #     opportunity = lost_leads.filtered(lambda r: r.type == 'opportunity')
        #
        # if filter_value == 'this_quater':
        #     print("yes")
        #     if current_month in first_quater:
        #         leads = lost_leads.filtered(lambda r: r.type == 'lead' and r.create_date.month in first_quater)
        #         print("leads first", leads)
        #         opportunity = lost_leads.filtered(lambda r: r.type == 'opportunity' and r.create_date.month in first_quater)
        #     else:
        #         leads = lost_leads.filtered(lambda r: r.type == 'lead' and r.create_date.month in second_quater)
        #         print("leads quater", leads)
        #         opportunity = lost_leads.filtered(
        #             lambda r: r.type == 'opportunity' and r.create_date.month in second_quater)

        return {
            'leads': len(leads),
            'opportunity': len(opportunity),
        }











