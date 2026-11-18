# ©  2026 Terrabit
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

from unittest.mock import patch

import psycopg2
from psycopg2 import errorcodes

from odoo.exceptions import ValidationError
from odoo.tests import Form, TransactionCase, tagged
from odoo.tools import mute_logger

from odoo.addons.l10n_md_zip import hooks
from odoo.addons.l10n_md_zip.models.res_partner import RELINK_PARAM

LOGGER = "odoo.addons.l10n_md_zip.models.res_partner"


class _LockNotAvailable(psycopg2.Error):
    pgcode = errorcodes.LOCK_NOT_AVAILABLE


class _CheckViolation(psycopg2.Error):
    pgcode = errorcodes.CHECK_VIOLATION


@tagged("post_install", "-at_install")
class TestCityFromZip(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.country = cls.env.ref("base.md")
        cls.Partner = cls.env["res.partner"]
        cls.state_balti = cls.env.ref("l10n_md_zip.state_md_ba")
        cls.state_anenii = cls.env.ref("l10n_md_zip.state_md_an")

    def _city(self, zip_code, name):
        return self.env["res.city"].search(
            [("country_id", "=", self.country.id), ("zipcode", "=", zip_code), ("name", "=", name)]
        )

    def _create_partner(self, name="Test Partner", zip_code="MD-3100", city="Balti"):
        return self.Partner.create({"name": name, "country_id": self.country.id, "city": city, "zip": zip_code})

    def test_data_loaded(self):
        """CA1: 37 states, cities enforced, MD-6501 lists three localities of Anenii Noi."""
        self.assertTrue(self.country.enforce_cities)
        states = self.env["res.country.state"].search([("country_id", "=", self.country.id)])
        self.assertEqual(len(states), 37)
        self.assertIn("Chișinău", states.mapped("name"))
        cities = self.env["res.city"].search([("country_id", "=", self.country.id), ("zipcode", "=", "MD-6501")])
        self.assertEqual(sorted(cities.mapped("name")), ["Anenii Noi", "Beriozchi", "Hirbovatul Nou"])
        self.assertEqual(cities.state_id, self.state_anenii)

    def test_unique_zip(self):
        """CA2: a postal code of a single locality gives the city and the state."""
        city, state = self.Partner._l10n_md_city_from_zip("MD-3100")
        self.assertEqual(city, self._city("MD-3100", "Balti"))
        self.assertEqual(state, self.state_balti)

    def test_zip_written_without_prefix(self):
        """CA3: 3100, MD3100 and md 3100 are read as MD-3100."""
        for typed in ("3100", "MD3100", "md 3100"):
            city, state = self.Partner._l10n_md_city_from_zip(typed)
            self.assertEqual(city, self._city("MD-3100", "Balti"), typed)
            self.assertEqual(state, self.state_balti, typed)

    def test_shared_zip_gives_state(self):
        """CA4: a postal code shared by several localities gives only the state; the city name picks one."""
        city, state = self.Partner._l10n_md_city_from_zip("MD-6501")
        self.assertFalse(city)
        self.assertEqual(state, self.state_anenii)
        city, state = self.Partner._l10n_md_city_from_zip("MD-6501", "BERIOZCHI")
        self.assertEqual(city, self._city("MD-6501", "Beriozchi"))

    def test_onchange_zip(self):
        """CA2, CA3: typing the postal code on the contact form fills in the address."""
        # not saved: other modules may make more fields required on the contact form
        partner_form = Form(self.Partner)
        partner_form.name = "Test Partner"
        partner_form.country_id = self.country
        partner_form.zip = "3100"
        self.assertEqual(partner_form.city_id, self._city("MD-3100", "Balti"))
        self.assertEqual(partner_form.city, "Balti")
        self.assertEqual(partner_form.zip, "MD-3100")
        self.assertEqual(partner_form.state_id, self.state_balti)

    def test_onchange_zip_already_linked(self):
        """CA3: retyping the postal code without MD- on a linked contact writes it back as MD-NNNN."""
        partner = self._create_partner()
        partner.l10n_md_fix_city_from_zip()
        partner_form = Form(partner)
        partner_form.zip = "3100"
        self.assertEqual(partner_form.zip, "MD-3100")
        self.assertEqual(partner_form.city_id, self._city("MD-3100", "Balti"))

    def test_onchange_shared_zip(self):
        """CA4: on the form, a shared postal code fills in only the state."""
        partner_form = Form(self.Partner)
        partner_form.name = "Test Partner"
        partner_form.country_id = self.country
        partner_form.zip = "MD-6501"
        self.assertFalse(partner_form.city_id)
        self.assertEqual(partner_form.state_id, self.state_anenii)

    def test_fix_city_from_zip(self):
        """CA5: the action links the contact to the city of its postal code."""
        partner = self._create_partner(zip_code="md3100")
        partner.l10n_md_fix_city_from_zip()
        self.assertRecordValues(
            partner,
            [
                {
                    "city_id": self._city("MD-3100", "Balti").id,
                    "city": "Balti",
                    "zip": "MD-3100",
                    "state_id": self.state_balti.id,
                }
            ],
        )
        # a second run changes nothing
        self.assertFalse(partner.l10n_md_fix_city_from_zip())

    def test_other_country_untouched(self):
        """CA5: a contact of another country is left as it is."""
        partner = self.Partner.create(
            {"name": "Ion Popescu", "country_id": self.env.ref("base.ro").id, "city": "Balti", "zip": "3100"}
        )
        partner.l10n_md_fix_city_from_zip()
        self.assertFalse(partner.city_id)
        self.assertFalse(partner.state_id)

    def test_basarabeasca(self):
        """CA7: the postal codes MD-67xx are in the district Basarabeasca."""
        cities = self.env["res.city"].search([("country_id", "=", self.country.id), ("zipcode", "=like", "MD-67%")])
        self.assertTrue(cities)
        self.assertEqual(cities.state_id, self.env.ref("l10n_md_zip.state_md_bs"))

    def test_relink_batch(self):
        """CA6: a batch relinks the contacts after the given id."""
        partner = self._create_partner()
        last_id, count = self.Partner._l10n_md_relink_batch(partner.id - 1)
        self.assertGreaterEqual(count, 1)
        self.assertTrue(partner.city_id)

    def test_relink_batch_limit(self):
        """CA6: a batch stops at its limit."""
        first = self._create_partner("Test Partner 1")
        second = self._create_partner("Test Partner 2")
        last_id, count = self.Partner._l10n_md_relink_batch(first.id - 1, limit=1)
        self.assertEqual((last_id, count), (first.id, 1))
        self.assertTrue(first.city_id)
        self.assertFalse(second.city_id)

    def test_cron_resumes_and_finishes(self):
        """CA6: the scheduled action resumes from its saved position, then deactivates itself."""
        params = self.env["ir.config_parameter"].sudo()
        partner = self._create_partner()
        cron_model = type(self.env["ir.cron"])
        params.set_int(RELINK_PARAM, partner.id - 1)
        with patch.object(cron_model, "_commit_progress", return_value=float("inf")) as progress:
            self.Partner._cron_l10n_md_relink_partners()
        self.assertTrue(partner.city_id)
        self.assertEqual(params.get_int(RELINK_PARAM), 0)
        progress.assert_called_with(remaining=0, deactivate=True)

    def test_post_init_hook_small_database(self):
        """CA6: on a small database the contacts are linked at install."""
        partner = self._create_partner()
        hooks.post_init_hook(self.env)
        self.assertTrue(partner.city_id)

    def test_post_init_hook_large_database_uses_cron(self):
        """CA6: on a large database the scheduled action is activated instead."""
        self._create_partner()
        cron = self.env.ref("l10n_md_zip.ir_cron_relink_partners")
        cron.active = False
        with patch.object(hooks, "RELINK_BATCH", 0):
            hooks.post_init_hook(self.env)
        self.assertTrue(cron.active)

    def _patch_write_failing_on(self, failing, error):
        """Make ``write`` raise ``error`` on any recordset that contains ``failing``."""
        partner_model = type(self.Partner)
        original_write = partner_model.write

        def write(records, vals):
            if failing in records:
                raise error
            return original_write(records, vals)

        return patch.object(partner_model, "write", write)

    def test_write_error_skips_only_that_contact(self):
        """A contact rejected by a constraint of another module does not stop the others."""
        good = self._create_partner("Test Partner Good")
        bad = self._create_partner("Test Partner Bad")
        for error in (ValidationError("rejected"), _CheckViolation("rejected")):
            with self.subTest(error=type(error).__name__):
                (good | bad).write({"city_id": False})
                with self._patch_write_failing_on(bad, error), mute_logger(LOGGER):
                    fixed = (good | bad).l10n_md_fix_city_from_zip()
                self.assertEqual(fixed, good)
                self.assertEqual(good.city_id, self._city("MD-3100", "Balti"))
                self.assertFalse(bad.city_id)

    def test_write_concurrency_error_is_raised(self):
        """A lock error is raised again, so that the whole batch is retried."""
        partner = self._create_partner()
        partner.city_id = False
        with self._patch_write_failing_on(partner, _LockNotAvailable("locked")), self.assertRaises(_LockNotAvailable):
            partner.l10n_md_fix_city_from_zip()
