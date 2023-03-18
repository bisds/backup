{
    'name': 'Ecosphere',
    'version': '15.0.0.2',
    'author': 'Ecosphere',
    'license': 'OPL-1',
    'website': 'https://foireecosphere.org/',
    'depends': ['base', 'contacts', 'mail', 'sms', 'l10n_ca', 'portal', 'mass_mailing'],
    'data': [
        'security/ir.model.access.csv',
        'views/contact_inherit_view.xml',
    ],
    'demo': [

    ],
    'qweb': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
