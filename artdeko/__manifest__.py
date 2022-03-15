# -*- coding: utf-8 -*-

{
    'name': 'ARTDEKO',
    'depends': [
        'base', 
        'base_setup',
        'contacts',
        'purchase',
        'sale',
        'product'
    ],
    'css': ['static/src/css/crm.css'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'data': [
        'security/ir.model.access.csv',
    ]
}