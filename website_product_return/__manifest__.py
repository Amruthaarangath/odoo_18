{
    'name': "Website Product Return ",
    'version': '1.0',
    'summary': 'Website Product Return',
    'description': "Website Product Return",
    'depends': ['base','sale', 'stock_account', 'website_sale', 'sale_management','web'],

    'data': [
        'data/sale_return_sequence.xml',
        'security/ir.model.access.csv',
        'views/website_product_return_inherit.xml',
        'views/sale_order_return_modal_view.xml',
        'views/submit_template_view.xml',
        'views/sale_return_view.xml',
        'views/stock_picking_view.xml',


    ],

        'assets': {
            'web.assets_frontend': [
                'website_product_return/static/src/js/sale_return.js',
            ],
        },


        'license': 'LGPL-3',
}
