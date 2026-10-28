from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.tests.common import tagged


@tagged('post_install_l10n', 'post_install', '-at_install')
class TestMoldovaChart(AccountTestInvoicingCommon):

    @classmethod
    @AccountTestInvoicingCommon.setup_chart_template('md')
    def setUpClass(cls):
        super().setUpClass()

    def _account(self, code):
        return self.env['account.account'].with_context(active_test=False).search([
            *self.env['account.account']._check_company_domain(self.env.company),
            ('code', '=', code),
        ], limit=1)

    def test_account_group_11_exists(self):
        account = self._account('112')
        self.assertTrue(account, 'Contul 112 (Imobilizări necorporale) nu a fost găsit')
        # În Odoo 20 grupele de conturi (account.group) sunt conturi părinte inactive
        group = account.parent_id
        self.assertEqual(group.code, '11')
        self.assertFalse(group.active)

    def test_vat_tax_exists(self):
        tax = self.env['account.tax'].search([
            *self.env['account.tax']._check_company_domain(self.env.company),
            ('name', '=', 'TVA 20%'),
            ('type_tax_use', '=', 'sale'),
        ], limit=1)
        self.assertTrue(tax, 'Taxa TVA 20% nu a fost găsită')
        self.assertEqual(tax.amount, 20.0)
