{
    'name': "CRM Dashboard ",
    'version': '1.0',
    'summary': 'CRM Dashboard',
    'description': "CRM Dashboard",
    'depends': ['base','crm','sales_team'],

    'data': [
        'views/sales_team_view.xml',
        'views/crm_dashboard_action_view.xml',

    ],

    'assets': {
        'web.assets_backend': [
            'crm_dashboard/static/src/js/dashboard.js',
            'crm_dashboard/static/src/xml/dashboard.xml'

        ],
    },

    'license': 'LGPL-3',
}
