# -*- coding: utf-8 -*-

{
    'name': 'ARTDEKO',
    'depends': [
        'base', 
        'base_setup',
        'contacts',
        'purchase',
        'sale',
        'stock'
    ],
    'css': ['static/src/css/crm.css'],
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
        'report/artdeko_reports.xml'
    ]
}