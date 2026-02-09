# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'test_migration',
    'version': '17.0.1.10',
    'category': 'Accounting/Accounting',
    'summary': 'Manage financial and analytic accounting',
    'depends': ['hr', 'hr_contract'], # Fondamentale: serve per vedere i menu HR
    'data': [
        'security/ir.model.access.csv',   # File per i permessi (crealo se non c'è)
        'views/hr_version_views.xml',     # Il file XML con la vista e il menu
    ],
    'installable': True,
    
}
