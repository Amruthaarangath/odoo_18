{
    'name': "Salesperson Filter tree View ",
    'version': '1.0',
    'summary': 'Salesperson Filter Tree View',
    'description': "Salesperson Filter Tree View",
    'depends': ['base', 'sale','web'],

    'data': [
        'views/salesperson_filter_view.xml',

    ],

    'assets': {
        'web.assets_backend': [
    'salesperson_filter_tree_view/static/src/xml/saleperson_filter_view_inherit.xml',
    'salesperson_filter_tree_view/static/src/js/salesperson_filter_view.js'
    ],
    },

    'license': 'LGPL-3',
}
