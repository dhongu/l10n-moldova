Loads the Moldovan localities with their postal code and district, and fills in the city and the
district of Moldovan addresses from the postal code.

- Ships the list of Moldovan localities with their postal code, linked to the 37 subdivisions of
  the Republic of Moldova (ISO 3166-2:MD: the districts, the municipalities Chișinău, Bălți and
  Bender, Găgăuzia and Stînga Nistrului), which the module adds as states of Moldova. The data
  comes from [GeoNames](https://www.geonames.org) (Creative Commons Attribution 4.0).
- Moldova is set to *enforce cities*: the city of a Moldovan address is chosen from the list.
- On the contact form, typing the postal code (cod poștal) of a Moldovan address sets the city and
  the district. The postal code can be typed as `MD-2001`, `MD2001` or `2001`: it is written back
  as `MD-2001`. A postal code shared by several localities sets only the district; the city name,
  when it matches one of them (without diacritics and case), picks the locality.
- The action *Moldova: set city from ZIP* on contacts links the Moldovan contacts to the city of
  their postal code and fills in the district.
- At install, the Moldovan contacts are linked: directly on a small database, by the scheduled
  action *Moldova: link contacts to the city of their ZIP* in batches on a large one (it
  deactivates itself when done).
