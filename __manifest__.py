# -*- coding: utf-8
{
    "name": "Planilla",
    "version": "1.0",
    "author": "Francisco Villegas",
    "category": "hr",
    "description": "Planilla",
    "website": "",
    "license": "AGPL-3",
    "depends": [
        'base',
        'hr',
        'hr_contract',
        'om_hr_payroll',
     ],
    "demo": [
    ],
    "data": [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'data/ini.xml',
        'view/hr_contract.xml',
        'view/hr_payslip.xml',
        'view/planilla.xml',
    ],
    'css': [],
    'test': [],
    "installable": True,
    'application': False,
}
