{
    'name': "Website Decimal Quantity",
    'version': '1.0',
    'summary': 'Website Decimal Quantity',
    'description': "Website Decimal Quantity",
    'depends': ['base', 'website', 'website_sale'],

    'data': [
              'views/website_decimal_quantity.xml',


    ],
'assets': {
        'web.assets_frontend': [
            'website_decimal_quantity/static/src/js/website_decimal_quantity.js'
        ],
    },
        'license': 'LGPL-3',
}
