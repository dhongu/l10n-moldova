# ©  2026 Terrabit
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).
{
    "name": "Moldova - City from ZIP",
    "summary": "Moldovan localities with postal code and district, filled in from the postal code",
    "version": "19.0.1.0.0",
    "author": "Terrabit",
    "website": "https://www.terrabit.ro",
    "category": "Localization",
    "countries": ["md"],
    "images": ["static/description/main_screenshot.png"],
    "license": "LGPL-3",
    "consultant_sheet": "full",
    "development_status": "Beta",
    "depends": ["base_address_extended"],
    "data": [
        "data/res_country_state_data.xml",
        "data/res.city.csv",
        "data/res_country_data.xml",
        "data/ir_actions_server.xml",
        "data/ir_cron.xml",
    ],
    "post_init_hook": "post_init_hook",
    "installable": True,
    "maintainers": ["dhongu"],
}
