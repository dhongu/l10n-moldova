# Șablonul planului de conturi MD (Ordinul MF nr. 119/2013), pe sistemul de
# chart template Odoo 19 — CSV-urile din data/template/ se încarcă automat
# pentru codul 'md' declarat aici.
from odoo import models
from odoo.addons.account.models.chart_template import template


class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    @template('md')
    def _get_md_template_data(self):
        return {
            'name': 'Moldova',
            'code_digits': '3',
            'property_account_receivable_id': 'pcg_221',
            'property_account_payable_id': 'pcg_521',
        }

    @template('md', 'res.company')
    def _get_md_res_company(self):
        return {
            self.env.company.id: {
                'account_fiscal_country_id': 'base.md',
                'bank_account_code_prefix': '242',
                'cash_account_code_prefix': '241',
                'transfer_account_code_prefix': '245',
                'income_currency_exchange_account_id': 'pcg_622',
                'expense_currency_exchange_account_id': 'pcg_722',
                'account_sale_tax_id': 'vat_20',
                'account_purchase_tax_id': 'vat_20_p',
                'income_account_id': 'pcg_611',
                'expense_account_id': 'pcg_711',
            },
        }
