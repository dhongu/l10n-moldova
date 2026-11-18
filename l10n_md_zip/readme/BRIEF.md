# Brief: l10n_md_zip

## Request

"pt moldova trebuie sa facem modulul" → "l10n_md_zip" (2026-11-17), after the shared
"More apps by Terrabit" list of the `l10n-*` repositories (dhongu/terrabit-pre-commit-hooks#15)
could not include Moldova: there was no Moldovan module to point to.

## Purpose

A company with customers or suppliers in the Republic of Moldova types their addresses by hand:
the city is spelled in several ways and the district is left empty. With the module, the postal
code of a Moldovan address fills in the locality and the district, like the other `l10n_xx_zip`
modules do for their country.

## Who operates

Whoever creates or edits contacts (sales, purchase, accounting), with the usual contact rights.
The action on the existing contacts is for *Contact: Creation* (`base.group_partner_manager`).

## Scope

- Repository and technical name: `dhongu/l10n-moldova`, `l10n_md_zip`.
- New module, built on the model of `l10n_pl_zip`, `l10n_de_zip`, `l10n_sk_zip`.
- `depends`: `base_address_extended` (the city of an address is chosen from `res.city`, and
  `enforce_cities` on the country).
- New models: none.
- Data: `res.country.state` for the 37 subdivisions of ISO 3166-2:MD (Odoo has none for Moldova),
  `res.city` for the localities with their postal code, `enforce_cities` on Moldova.
- Standard models extended: `res.partner` (onchange of the postal code, action, scheduled action),
  no new fields.

## Flow

1. Open **Contacts → Configuration → Localization → Cities** and search a postal code: the
   Moldovan localities of that postal code are listed with their district.
2. On a contact in Moldova, type the postal code: the city and the district are filled in.
3. When the postal code is shared by several localities, only the district is filled in; the city
   is chosen from the list.
4. Select existing Moldovan contacts and run *Actions → Moldova: set city from ZIP*.

## Acceptance criteria

- **CA1:** After install, Moldova has the 37 subdivisions of ISO 3166-2:MD as states (32 districts,
  the municipalities Chișinău, Bălți, Bender, Găgăuzia and Stînga Nistrului), Moldova enforces
  cities, and the list of cities searched on `MD-6501` shows Anenii Noi, Beriozchi and
  Hirbovatul Nou, all in the district Anenii Noi.
- **CA2:** On a contact in Moldova, typing the postal code `MD-3100` sets the city Balti and the
  state Bălți.
- **CA3:** Typing `3100`, `MD3100` or `md 3100` gives the same result as `MD-3100`, and the postal
  code is rewritten as `MD-3100`.
- **CA4:** Typing `MD-6501` (shared by three localities of Anenii Noi) sets only the state Anenii
  Noi; with the city already typed as `BERIOZCHI`, the locality Beriozchi is chosen.
- **CA5:** *Actions → Moldova: set city from ZIP* on Moldovan contacts links them to the city of
  their postal code and fills in the state; a contact of another country is left as it is.
- **CA6:** At install, the Moldovan contacts are linked to their city; on a large database the
  scheduled action *Moldova: link contacts to the city of their ZIP* is activated instead, works in
  batches and deactivates itself when done.
- **CA7:** The postal codes `MD-67xx` are in the district Basarabeasca (GeoNames still files them
  under Cimișlia).

## Edge cases

- Multi-company: the cities and states are shared data, as in Odoo.
- A contact that cannot be written (constraint of another module) is logged and skipped; the
  others are linked.
- A contact of type *contact* takes the address of its parent: it is relinked through its parent.
- Running the action twice changes nothing the second time.

## Decisions taken

| Decision | Choice | Reason |
|---|---|---|
| Source of the localities | GeoNames postal codes, CC BY 4.0 | Same source as the other `l10n_xx_zip` modules; the only free list with postal codes for Moldova. |
| States | The module creates the 37 ISO 3166-2:MD subdivisions | Asked (2026-11-17); Odoo defines none for Moldova, as for FR, CZ, SK. |
| Left bank of the Dniester | Localities in *Stînga Nistrului* (SN), Bender in *Bender* (BD) | The ISO 3166-2:MD subdivisions. |
| Basarabeasca | `MD-67xx` in Basarabeasca, not Cimișlia | GeoNames keeps the district split before 2003. |
| Names of the localities | As in GeoNames, without diacritics | The match ignores diacritics and case; correcting 1,700 names by hand is not checkable here. |
| Repository | `dhongu/l10n-moldova`, with the repository scaffold of `l10n-poland` | Asked (2026-11-17); same branches (19.0/20.0) as the other `l10n-*` repositories. |
| Documentation language | English, `i18n/ro.po` for Romanian | Convention of the `l10n_xx_zip` modules; Romanian is the official language of Moldova. |

## Open decisions

None.

## Out of scope

- Romanian diacritics in the names of the localities.
- Streets and the postal codes of streets in Chișinău.
- A Russian translation.
- Banks, e-invoicing and the chart of accounts (`l10n_md`).
