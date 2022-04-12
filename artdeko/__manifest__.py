# -*- coding: utf-8 -*-

{
    'name': 'ARTDEKO',
    'depends': [
        'base', 
        'base_setup',
        'contacts',
        'purchase',
        'sale',
        'stock',
        'account',
        'sale_stock'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'data': [
        'security/ir.model.access.csv',
        'views/artdeko_views.xml',
        'views/users_views.xml',
        'views/stock_picking_views.xml',
        'views/sale_order_views.xml',
        'report/artdeko_paper_formats.xml',
        'report/artdeko_layouts.xml',
        'report/artdeko_sale_templates.xml',
        'report/artdeko_purchase_order_templates.xml',
        'report/artdeko_reports.xml'
    ],
    'assets': {
        'web.report_assets_common': [
            '/artdeko/static/src/css/rockwell_regular_base64.css',
            '/artdeko/static/src/css/lato_regular_base64.css',
            '/artdeko/static/src/css/lato_regular_base64.css'
        ],
    },
}