{
    'name': "Clear Cart",
    'version': '1.0',
    'summary': 'Clear Cart',
    'description': "Clear Cart",
    'depends': ['base', 'website','sale','website_sale'],

'data': [
              'views/website_clear_cart_view.xml',
],
'assets': {
        'web.assets_frontend': [
            'clear_cart/static/src/js/clear_cart.js'
        ],
    },
        'license': 'LGPL-3',
}

