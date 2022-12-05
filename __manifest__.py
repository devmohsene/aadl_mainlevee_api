# -*- coding: utf-8 -*-
{
    'name': "aadl_mainlevee_api",

    'summary': """
       API du module aadl_acts fourni un api pour l'application mobule""",

    'description': """
        fourni un api pour l'application mobule
    """,

    'author': "DJELLAB MOHSENE",
    'website': "http://www.aadl.com.dz",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['aadl_acts'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'views/views.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],

    'application' : True,
}