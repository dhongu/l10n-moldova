from odoo.tests.common import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestMoldovaChart(TransactionCase):

    def test_account_group_11_exists(self):
        account = self.env['account.account'].search([('code', '=', '112')], limit=1)
        self.assertTrue(account, 'Contul 112 (Imobilizări necorporale) nu a fost găsit')

    def test_vat_tax_exists(self):
        tax = self.env['account.tax'].search([('name', '=', 'TVA 20%')], limit=1)
        self.assertTrue(tax, 'Taxa TVA 20% nu a fost găsită')
        self.assertEqual(tax.amount, 20.0)

    def test_bank_list_loaded(self):
        count = self.env['res.bank'].search_count([('country.code', '=', 'MD')])
        self.assertTrue(count > 0, 'Nu există bănci moldovenești încărcate')
