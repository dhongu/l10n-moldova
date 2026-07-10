{
    'name': 'Moldova - Accounting',
    'website': 'https://mf.gov.md/',
    'author': 'Terrabit',
    'icon': '/account/static/description/l10n.png',
    'countries': ['md'],
    'category': 'Accounting/Localizations/Account Charts',
    'version': '19.0.1.0.0',
    'depends': [
        'account',
        'base_vat',
    ],
    'auto_install': False,
    'description': """
Modul de localizare contabilă pentru Republica Moldova.

Planul de conturi (conturi de gradul I) e extras din Planul general de conturi
contabile aprobat prin Ordinul Ministerului Finanțelor nr. 119 din 06.08.2013
(https://mf.gov.md/sites/default/files/legislatie/Planul%20general%20de%20conturi%20contabile.pdf).

Cotele de taxe (TVA 20%/8%/0%, impozit pe profit 12%, asigurări sociale 24%,
asigurare medicală 9%) sunt conform Codului Fiscal al Republicii Moldova.
""",
    'data': [
        'views/res_company_view.xml',
        'data/res.bank.csv',
        'data/template/account.group-md.csv',
        'data/template/account.account-md.csv',
        'data/template/account.tax.group-md.csv',
        'data/template/account.tax-md.csv',
        'data/template/account.journal-md.csv',
        'data/template/account.payment.term-md.csv',
        'data/template/account.fiscal.position-md.csv',
    ],
    'demo': [
        'demo/demo_company.xml',
    ],
    'license': 'LGPL-3',
}
