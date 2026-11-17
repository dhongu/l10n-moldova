1. As an administrator, open **Contacts → Configuration → Localization → Cities** and search
   for a postal code, for example `MD-6501`: the Moldovan localities of that postal code are listed
   with their district in the **State** column.

   ![Cities list filtered on the postal code MD-6501: Anenii Noi, Beriozchi and Hirbovatul Nou, all with the country Moldova and the state Anenii Noi (MD)](static/description/en/01_lista_localitati_cap.png)

2. Open a contact with the country **Moldova** and type the postal code in the address, for example
   `MD-3100`: the city and the state are filled in. The code can also be typed as `3100`, `MD3100`
   or `md 3100`; when the locality is identified, it is written back as `MD-3100`.

   ![Contact Example Balti SRL in Moldova: the postal code MD-3100 fills in the city Balti (MD-3100) and the state Bălți (MD)](static/description/en/02_partener_cap_unic.png)

3. When the postal code is shared by several localities (`MD-6501`), only the state is filled in
   (when the localities are all in the same district); choose the city from the list (type the
   postal code or the name in the **City** field). When the contact already has the city name, for
   example *BERIOZCHI*, that locality is chosen by itself (diacritics and letter case are ignored).

   ![Contact Example Anenii Noi SRL: the postal code MD-6501 fills in the state Anenii Noi (MD); the City field lists Anenii Noi, Beriozchi and Hirbovatul Nou, all with MD-6501](static/description/en/03_partener_cap_comun.png)

4. To complete existing or imported contacts, select them in the list view of **Contacts** and run
   **Actions → Moldova: set city from ZIP** (right *Contact: Creation*). Select the companies, not
   their contact persons: a contact person takes the address of its company. Contacts of other
   countries are left as they are.

   ![Contacts list with 7 contacts selected and the Actions menu open; its last row is Moldova: set city from ZIP](static/description/en/04_actiune_contacte_existente.png)

   After the action, a contact imported with the code `6501` and the city *Beriozchi* has the code
   `MD-6501`, the city *Beriozchi* and the state *Anenii Noi*.

   ![Contact Customer Beriozchi after the action: ZIP MD-6501, city Beriozchi (MD-6501) and state Anenii Noi (MD)](static/description/en/05_contact_dupa_actiune.png)

At install, the Moldovan contacts that have a postal code are linked to their city: directly on a
small database, or by the scheduled action *Moldova: link contacts to the city of their ZIP*, in
batches, on a large one (it deactivates itself when done).

The names of the localities come from GeoNames without diacritics (*Balti*, *Durlesti*); the
states have them (*Bălți*, *Chișinău*).
