# -*- coding: utf-8 -*-

{
    'name': 'EESTISOFT partner multiparent',
    'summary': "This module adds multiple parents to partner",
    'version': '12.0.1',
    'author': 'EESTISOFT, ' 'Hideki Yamamoto',
    'license': "AGPL-3",
    'maintainer': 'EESTISOFT, ''Hideki Yamamoto',
    'category': 'productivity',
    'website': "http://www.eestisoft.com",
    'depends': ['base_setup','contacts'],
    'data': ['data/ees_multiparent.xml',	
        'data/ir.model.access.csv'],
    'auto_install': False,
    'installable': True,
    'application': True
}