# -*- coding: utf-8 -*-
{
    'name': 'Objetos Perdidos - School Lost & Found',
    'version': '17.0.1.0.0',
    'category': 'School',
    'summary': 'Gestión de objetos perdidos para centros educativos',
    'description': """
        Módulo para gestionar los objetos perdidos de un centro escolar.
        Permite registrar objetos, asignar categorías y entregar objetos a alumnos
        mediante su NIA. Incluye portal web para consulta pública.
    """,
    'author': 'Senior Odoo Developer',
    'website': 'https://www.example.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
        'website',
    ],
    'data': [
        # Security
        'security/security.xml',
        'security/ir.model.access.csv',
        # Views
        'views/school_student_views.xml',
        'views/lost_object_category_views.xml',
        'views/lost_object_views.xml',
        'views/lost_object_wizard_views.xml',
        'views/menus.xml',
        # Website Templates
        'views/website_templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'school_lost_found/static/src/css/portal.css',
        ],
    },
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
