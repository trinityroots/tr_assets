# -*- coding: utf-8 -*-
{
    'name': "Assets Management",

    'summary': """
        This module is for managing assets.""",

    'description': """
        This module is for managing assets...
    """,

    'author': "Patiphol P., Trinity Roots Co., Ltd.",
    'website': "http://www.trinityroots.co.th",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Website',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/assets.xml',
        'views/templates.xml',
        'views/assets_color.xml',
        'views/assets_type.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}