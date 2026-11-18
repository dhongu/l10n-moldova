#!/usr/bin/env python3
# ©  2026 Terrabit
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).
"""Generate the data of l10n_<cc>_zip from the GeoNames postal codes of the country.

Usage: python3 scripts/generate_city_data.py <path to XX.txt>

XX.txt comes from https://download.geonames.org/export/zip/XX.zip (GeoNames,
Creative Commons Attribution 4.0); the country is read from the file name (PL.txt,
DE.txt, FR.txt, ES.txt, CZ.txt, SK.txt, MD.txt). Columns: country, postal code, place name,
region, region code, province, province code, ...

Writes, in l10n_<cc>_zip/data:
- res.city.csv: the localities, linked to the regions of the country;
- res_country_state_data.xml: the regions, only for the countries where Odoo does not
  define them (FR departments, CZ and SK regions, MD districts). PL, DE and ES use the states of Odoo.
"""

import csv
import re
import sys
from pathlib import Path

PL_STATES = {"72": "ds", "73": "kp", "74": "ld", "75": "lb", "76": "ls", "77": "mp", "78": "mz", "79": "op",
             "80": "pk", "81": "pl", "82": "pm", "83": "sl", "84": "sk", "85": "wm", "86": "wp", "87": "zp"}  # fmt: skip
# GeoNames region code -> (ISO 3166-2 code, name)
CZ_STATES = {
    "52": ("10", "Hlavní město Praha"), "88": ("20", "Středočeský kraj"), "79": ("31", "Jihočeský kraj"),
    "87": ("32", "Plzeňský kraj"), "81": ("41", "Karlovarský kraj"), "89": ("42", "Ústecký kraj"),
    "83": ("51", "Liberecký kraj"), "82": ("52", "Královéhradecký kraj"), "86": ("53", "Pardubický kraj"),
    "80": ("63", "Kraj Vysočina"), "78": ("64", "Jihomoravský kraj"), "84": ("71", "Olomoucký kraj"),
    "90": ("72", "Zlínský kraj"), "85": ("80", "Moravskoslezský kraj"),
}  # fmt: skip
SK_STATES = {
    "BL": "Bratislavský kraj", "TA": "Trnavský kraj", "TC": "Trenčiansky kraj", "NI": "Nitriansky kraj",
    "ZI": "Žilinský kraj", "BC": "Banskobystrický kraj", "PV": "Prešovský kraj", "KI": "Košický kraj",
}  # fmt: skip

# ISO 3166-2:MD: the districts (raioane), the municipalities, the autonomous territorial unit
# of Gagauzia and the territorial units of the left bank of the Dniester
MD_STATES = {
    "AN": "Anenii Noi", "BS": "Basarabeasca", "BR": "Briceni", "CA": "Cahul", "CT": "Cantemir",
    "CL": "Călărași", "CS": "Căușeni", "CM": "Cimișlia", "CR": "Criuleni", "DO": "Dondușeni",
    "DR": "Drochia", "DU": "Dubăsari", "ED": "Edineț", "FA": "Fălești", "FL": "Florești",
    "GL": "Glodeni", "HI": "Hîncești", "IA": "Ialoveni", "LE": "Leova", "NI": "Nisporeni",
    "OC": "Ocnița", "OR": "Orhei", "RE": "Rezina", "RI": "Rîșcani", "SI": "Sîngerei",
    "SO": "Soroca", "ST": "Strășeni", "SD": "Șoldănești", "SV": "Ștefan Vodă", "TA": "Taraclia",
    "TE": "Telenești", "UN": "Ungheni", "BA": "Bălți", "BD": "Bender", "CU": "Chișinău",
    "GA": "Găgăuzia", "SN": "Stînga Nistrului",
}  # fmt: skip
# GeoNames region name (without diacritics, with its typos) -> ISO 3166-2:MD code
MD_REGIONS = {
    "Anenii Noi": "AN", "Briceni": "BR", "Cahul": "CA", "Canul": "CA", "Cantemir": "CT",
    "Cantrmir": "CT", "Calarasi": "CL", "Causeni": "CS", "Cimislia": "CM", "Criuleni": "CR",
    "Donduseni": "DO", "Drochia": "DR", "Lazo": "DR", "Dubasari Cr.": "DU", "Criuleni-Dub.": "DU",
    "Criuleni- Dub.": "DU", "Criulenii-Dub.": "DU", "Edinet": "ED", "Falesti": "FA",
    "Floresti": "FL", "Glodeni": "GL", "Hincesti": "HI", "Ialoveni": "IA", "Leova": "LE",
    "Nisporeni": "NI", "Ocnita": "OC", "Orhei": "OR", "Rezina": "RE", "Riscani": "RI",
    "Singerei": "SI", "Soroca": "SO", "Straseni": "ST", "Soldanesti": "SD", "Stefan-Voda": "SV",
    "Taraclia": "TA", "Telenesti": "TE", "Ungheni": "UN", "Uhnheni": "UN", "Balti": "BA",
    "Mun.Balti": "BA", "Bender Tr.": "BD", "Mun.Chisinau": "CU", "Comrat": "GA",
    "Ribnita Tr.": "SN", "Grigoriopol Tr.": "SN", "Slobozia Tr.": "SN", "Dubasari Tr.": "SN",
    "Camenca Tr.": "SN", "Tiraspol Tr.": "SN",
}  # fmt: skip


def state_of(cc, row, states):
    """Return the xml id of the region of a GeoNames row (and remember the ones to create)."""
    region_code, province_name, province_code = row[4].strip(), row[5].strip(), row[6].strip()
    if cc == "pl":
        return f"base.state_pl_{PL_STATES[region_code]}" if region_code in PL_STATES else None
    if cc == "de":
        return f"base.state_de_{region_code.lower()}" if region_code else None
    if cc == "es":
        # Odoo names Melilla (code ME) state_es_ml
        return f"base.state_es_{'ml' if province_code == 'ME' else province_code.lower()}" if province_code else None
    if cc == "fr":
        if not province_code:
            return None
        states[f"state_fr_{province_code.lower()}"] = (province_code, province_name)
        return f"state_fr_{province_code.lower()}"
    if cc == "cz" and region_code in CZ_STATES:
        code, name = CZ_STATES[region_code]
        states[f"state_cz_{code}"] = (code, name)
        return f"state_cz_{code}"
    if cc == "sk" and region_code in SK_STATES:
        states[f"state_sk_{region_code.lower()}"] = (region_code, SK_STATES[region_code])
        return f"state_sk_{region_code.lower()}"
    if cc == "md":
        code = MD_REGIONS.get(" ".join(row[3].split()))
        # GeoNames still files Basarabeasca (postal codes MD-67xx) under Cimislia, as before 2003
        if row[1].startswith("MD-67"):
            code = "BS"
        if not code:
            return None
        states[f"state_md_{code.lower()}"] = (code, MD_STATES[code])
        return f"state_md_{code.lower()}"
    return None


def main(source):
    cc = Path(source).stem.lower()
    root = Path(__file__).resolve().parent.parent / f"l10n_{cc}_zip" / "data"
    rows, states = set(), {}
    with open(source, encoding="utf-8", newline="") as handle:
        for row in csv.reader(handle, delimiter="\t"):
            if len(row) < 7 or row[0] != cc.upper():
                continue
            zip_code, name = row[1].strip(), row[2].strip()
            if cc == "fr" and not re.fullmatch(r"\d{5}", zip_code):
                continue  # the CEDEX codes ("01101 CEDEX") are not the postal code of an address
            state = state_of(cc, row, states)
            if zip_code and name and state:
                rows.add((zip_code, name, state))
    counter = {}
    with open(root / "res.city.csv", "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["id", "country_id:id", "zipcode", "name", "state_id:id"])
        for zip_code, name, state in sorted(rows):
            key = re.sub(r"\W", "", zip_code)
            index = counter.get(key, 0)
            counter[key] = index + 1
            writer.writerow([f"{cc}_city_{key}_{index}", f"base.{cc}", zip_code, name, state])
    if states:
        xml = ['<?xml version="1.0" encoding="utf-8" ?>', "<odoo>"]
        for xml_id, (code, name) in sorted(states.items()):
            xml += [
                f'    <record id="{xml_id}" model="res.country.state">',
                f'        <field name="country_id" ref="base.{cc}" />',
                f'        <field name="code">{code}</field>',
                f'        <field name="name">{name.replace("&", "&amp;")}</field>',
                "    </record>",
            ]
        xml += ["</odoo>", ""]
        (root / "res_country_state_data.xml").write_text("\n".join(xml), encoding="utf-8")
    print(f"{len(rows)} cities written")  # pylint: disable=print-used


if __name__ == "__main__":
    main(sys.argv[1])
