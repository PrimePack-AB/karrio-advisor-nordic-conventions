# Design

## Context

`lanes.lane_of` already reduces a request to a lane with `to_norway` and `voec_number` (`customs.options.voec_number`), and `advisor_nordic_conventions_dhl_freight_sweden_voec_marking` is the only rule that reads them.
The VOEC scheme's applicability depends on three facts the request carries: each commodity's `hs_code`, its `value_amount` and `value_currency`, and the recipient's `federal_tax_id` and `state_tax_id`.
The three new rules apply on every carrier and origin `lane_of` admits, so they join the Across carriers group.
All three fire only when the lane goes to Norway and `voec_number` is set, so a consumer that does not use VOEC sees nothing new.

## Rule placement

The three rules live in a new `rules/voec.py`, registered in `procedures.RULES` after `customs_values.zero_value_line` and mapped to the empty answering set in `procedures.ANSWERING`.
The exchange rate table and its date live in a new `rates.py`, because they are data with their own refresh cycle; the `Source` objects that cite them stay in `sources.py` with the others.
The HS class table lives in `rules/voec.py` beside the rule that reads it, since nothing else uses it.

## Item naming

A triggering commodity is named by `description`, else `title`, else `sku`, else `line <index>`.
`description` comes first because it is the text declared to customs and the one a customs officer or the shipper's staff compares with the parcel; `title` and `sku` are the shop's identifiers.
Both value and goods advisories also list zero-based indexes under `details.lines`, as `zero_value_line` and `ch_discount_on_invoice` do.

## HS classifier

No official mapping from HS codes to the VOEC exclusions exists.
The legal tests are functional: a foodstuff is any good meant for human consumption (merverdiavgiftsloven § 5-2 (2), merverdiavgiftsforskriften § 5-2-1 (1)), and the other exclusions are goods requiring an import permit and goods subject to excise duties (merverdiavgiftsloven § 3-1 (2)).
The classifier is therefore a heuristic over tariff chapters and headings, tagged I, that approximates those tests for the goods most often sold to consumers.
It reads `hs_code` as its digits only, matches the longest listed prefix (headings before chapters), needs four digits for a heading match and two for a chapter match, and leaves a commodity without an `hs_code` unclassified.
There is no description-keyword fallback, so an unlabelled food item is silent.
The classifier omits, by design, excise goods other than alcohol and tobacco (sugar, beverage packaging, lubricating oil, HFC and PFC goods), and restricted goods outside the listed chapters (plants, seeds, animals, CITES goods, waste, explosives and fireworks, cultural objects).

The heading texts below are Tolletaten's tariff structure dataset, `tolltariffstruktur.json` version 1.5, last modified 2026-06-23, retrieved 2026-10-16 (`TOLLTARIFF_STRUCTURE_URL`).

| HS prefix | Class | Tolltariffen heading text | Rationale (I) |
|---|---|---|---|
| 02, 03, 04 | foodstuffs | 02 "Kjøtt og spiselig slakteavfall"; 03 "Fisk og krepsdyr, bløtdyr og andre virvelløse dyr som lever i vann"; 04 "Melk og meieriprodukter; fugleegg; naturlig honning; spiselige produkter av animalsk opprinnelse, ikke nevnt eller innbefattet annet sted" | Edible animal products; mval § 5-2 (2) "enhver mat- eller drikkevare"; Tolletaten example "mat". |
| 07, 08, 09, 10, 11 | foodstuffs | 07 "Grønnsaker, røtter og knoller, spiselige"; 08 "Spiselige frukter og nøtter; skall av sitrusfrukter eller meloner"; 09 "Kaffe, te, maté og krydderier"; 10 "Korn"; 11 "Mølleprodukter; malt; stivelse; inulin; gluten av hvete" | Edible plant products, coffee, tea, and spices; mval § 5-2 (2). |
| 12 except 1209 | foodstuffs | "Oljeholdige frø og frukter; forskjellige andre frø og frukter; planter til industriell eller medisinsk bruk; halm og fôrplanter" | Mostly edible seeds and herbs; 1209 "Frø, frukter og sporer av det slag som brukes som såvarer" is seed for sowing, not for consumption, and is left unclassified. 1211 (plants for perfumery and pharmacy) stays in, an accepted false-positive risk. |
| 13 | foodstuffs | "Skjellakk og liknende; naturlige gummier, harpikser og andre vegetabilske safter og ekstrakter" | Mostly food additives and extracts (1302 pectin, agar); 1301 shellac and gums stays in, an accepted false-positive risk. |
| 15 except 1518, 1520, 1521, 1522 | foodstuffs | "Animalske, vegetabilske eller mikrobielle oljer og fettstoffer samt spaltningsprodukter derav; tilberedt spisefett; animalsk og vegetabilsk voks" | Edible fats and oils; 1518 (chemically modified fats), 1520 "Glyserol, rå", 1521 "Vegetabilsk voks … bivoks", and 1522 "Degras; reststoffer" are not for consumption and are left unclassified. |
| 16, 17, 18, 19, 20, 21 | foodstuffs | 16 "Produkter av kjøtt, flesk, fisk, …"; 17 "Sukker og sukkervarer"; 18 "Kakao og varer derav"; 19 "Produkter av korn, mel, stivelse eller melk; bakverk"; 20 "Produkter av grønnsaker, frukter, nøtter og andre plantedeler"; 21 "Forskjellige tilberedte næringsmidler" | Prepared foods; 2106 "Tilberedte næringsmidler, ikke nevnt eller innbefattet annet sted" carries food supplements, matching Tolletaten's "kosttilskudd" and the guidelines' "nutritional and dietary supplements". |
| 2201, 2202 | foodstuffs | 2201 "Vann, herunder naturlig eller kunstig mineralvann og karbonisert vann, ikke tilsatt sukker, …"; 2202 "Vann, … tilsatt sukker, … og andre alkoholfrie drikkevarer, …" | Non-alcoholic beverages; mval § 5-2 (2) "drikkevare", Tolletaten example "drikke". |
| 2209 | foodstuffs | "Eddik samt eddikerstatninger fremstilt av eddiksyre." | Vinegar is a food ingredient; mval § 5-2 (2). |
| 2936 | foodstuffs | "Provitaminer og vitaminer, naturlige eller syntetisk reproduserte (herunder naturlige konsentrater), …" | Tolletaten example "vitaminer"; vitamins sold as medicines are restricted goods instead, which the advisory also excludes. |
| 2203-2208 | alcohol | 2203 "Øl fremstilt av malt."; 2204 "Vin av friske druer, …"; 2205 "Vermut …"; 2206 "Andre gjærede drikkevarer …"; 2207 "Udenaturert etylalkohol med alkoholstyrke minst 80 volumprosent; etylalkohol og brennevin, denaturert, …"; 2208 "Udenaturert etylalkohol med alkoholstyrke under 80 volumprosent, likør og annet brennevin." | Excise goods (særavgiftsforskriften kap. 3-2 and 3-3) and restricted goods; guidelines §3 "alcoholic beverages", Tolletaten "alkohol". |
| 24 | tobacco | "Tobakk og varer framstilt av tobakkerstatninger; produkter, også med innhold av nikotin, ment for inhalering uten forbrenning; andre nikotinholdige produkter …" | Excise goods (særavgiftsforskriften kap. 3-1) and restricted goods; guidelines §3 "tobacco products", Tolletaten "tobakk". |
| 30 | pharmaceuticals | "Farmasøytiske produkter" | Restricted goods; guidelines §3 "Importation of medicinal drugs is restricted", Tolletaten "legemidler"; mval § 5-2 (3) excludes "legemidler" from foodstuffs. |
| 93 | arms and ammunition | "Våpen og ammunisjon; deler og tilbehør dertil" | Restricted goods; Tolletaten "våpen", guidelines appendix "Weapons, weapons parts, and ammunition". |

Chapters 01 "Levende dyr", 05 "Produkter av animalsk opprinnelse, ikke nevnt eller innbefattet annet sted", 06 "Levende trær og andre planter; …", and 14 "Vegetabilske flettematerialer; …" are not goods meant for human consumption and are left unclassified.
Chapter 23 "Reststoffer og avfall fra næringsmiddelindustrien; tilberedt dyrefôr" is animal feed and residues, not for human consumption, and is left unclassified.
Live animals, plants, and seeds for sowing are restricted goods per the guidelines' appendix (p.18, "Foodstuffs, plants, seeds, animals"), so leaving them unclassified is a known gap rather than a ruling that they are in scope; see Open questions.

## Value threshold and exchange rates

karrio's `Commodity.value_amount` is the value of one unit: the SDK's `units.Products.value_amount` sums `item.value_amount * item.quantity` (karrio `modules/sdk/karrio/core/units.py:673-681`), and both connectors in scope declare `value_amount * (quantity or 1)` per line (karrio-postnord `shipment/create.py:373`, karrio-dhl-freight-sweden `shipment/create.py:662`).
The rule therefore compares `value_amount` itself, not `value_amount / quantity`, with the limit.
The guidelines §4 make the value "at point of sale" decisive and §10.5 and mvaf § 1-3-8 (2)-(3) let the seller use any Norges Bank, Tolletaten, or market rate published within 30 days before payment, so the plugin cannot know the rate the seller used.

`rates.py` holds one rate per currency, NOK per unit, from Norges Bank's EXR dataset (spot, ECB concertation time 14:15 CET), retrieved 2026-10-16 from `https://data.norges-bank.no/api/data/EXR/B.EUR+SEK+DKK+USD.NOK.SP?format=csv&lastNObservations=1&locale=en` (`NORGES_BANK_EXR_URL`).
SEK and DKK are quoted per 100 units (`UNIT_MULT` 2) and are stored per unit.

| Currency | Norges Bank observation | Rate date | NOK per unit | Unit value converting to about NOK 3,150 |
|---|---|---|---|---|
| SEK | 95.31 per 100 | 2026-10-15 | 0.9531 | SEK 3,305.0 |
| EUR | 10.652 | 2026-10-15 | 10.652 | EUR 295.72 |
| DKK | 142.5 per 100 | 2026-10-15 | 1.425 | DKK 2,210.5 |
| USD | 9.5039 | 2026-10-15 | 9.5039 | USD 331.45 |
| NOK | identity | — | 1.0 | NOK 3,000 (no margin) |

The 5 % margin is a design choice, not a sourced fact.
It absorbs the difference between the static table and the rate the seller used at the point of sale, which may be up to 30 days old and from another publisher, so the advisory fires only when an item is clearly over and does not flag an item the seller correctly priced below NOK 3,000.
A NOK value needs no conversion, so it is compared with 3,000 itself; a NOK 3,000 item is at the limit whatever rate anyone used.
A refresh replaces the rates and the rate date together, updates `NORGES_BANK_EXR_URL`'s annotation and the footnote, and is an annotation-and-data change with no spec change.

## Business recipient

The B2B guide says a buyer that claims to be a business is not charged VAT and that the seller does not have to prove the claim; a recipient tax id is the request's only trace of such a claim.
The rule fires on any non-blank `federal_tax_id` or `state_tax_id` and does not check the nine-digit, 8-or-9 organisation number format the guide describes, because consumers store VAT numbers in several shapes (`912345678`, `NO912345678MVA`) and a format check would silence real business recipients.

## Sources and evidence classes

The evidence classes are those of `sources.EVIDENCE_TAGS` and the facts note `FACTS_NOTE` they come from: S is repository code or vendored specification, W is public carrier or authority documentation, and I is inference.
Every quoted statement below is W, read verbatim from the official document on 2026-10-16; every HS-to-class row above is I.
No new source cites `FACTS_NOTE`, because none of these facts is recorded in the facts note.

New document constants, each with a footnote in `docs/concepts/advisories.md`:

- `SKE_VOEC_GUIDELINES_URL`: Skatteetaten, "Sell, charge and ship goods to Norway – Guidelines for VAT On Electronic Commerce (VOEC)", <https://www.skatteetaten.no/globalassets/bedrift-og-organisasjon/voec/sell-charge-and-ship-goods-to-norway.pdf>, PDF modified 2025-03-28, read 2026-10-16.
- `SKE_VOEC_B2B_URL`: Skatteetaten, "Guide for sellers in the VOEC scheme – how to treat B2B sales", <https://www.skatteetaten.no/globalassets/bedrift-og-organisasjon/voec/how-to-treat-b2b-sales-2026.pdf>, PDF created 2026-02-04, read 2026-10-16.
- `TOLL_VOEC_PAGE_URL`: Tolletaten, "Om VOEC-ordningen", <https://www.toll.no/no/bedrift/import/voec/om-voec-ordningen>, oppdatert 2025-11-27, read 2026-10-16.
- `MVAL_URL`: Lovdata, merverdiavgiftsloven (LOV-2009-06-19-58), <https://lovdata.no/dokument/NL/lov/2009-06-19-58>, sist endret LOV-2025-12-22-121 fra 2026-07-01, read 2026-10-16.
- `MVAF_URL`: Lovdata, merverdiavgiftsforskriften (FOR-2009-12-15-1540), <https://lovdata.no/dokument/SF/forskrift/2009-12-15-1540>, sist endret FOR-2026-06-26-1398 fra 2026-07-01, read 2026-10-16.
- `TOLLTARIFF_STRUCTURE_URL`: Tolletaten open data, "Tolltariff struktur", <https://data.toll.no/dataset/6350e783-b989-4c7c-9ec0-de2dcb97363c/resource/68f78255-cbb0-4e75-86b1-3d5928816903/download/tolltariffstruktur.json>, version 1.5, last modified 2026-06-23, read 2026-10-16.
- `NORGES_BANK_EXR_URL`: as above, rates for 2026-10-15, read 2026-10-16.

New `Source` objects: `SKE_VOEC_EXCLUDED_GOODS`, `SKE_VOEC_PER_ITEM_THRESHOLD`, `SKE_VOEC_MIXED_CONSIGNMENT`, `SKE_VOEC_B2C_ONLY`, `SKE_VOEC_B2B`, `TOLL_VOEC_EXCLUDED_GOODS`, `TOLL_VOEC_PER_ITEM_THRESHOLD`, `MVAL_LOW_VALUE_EXCLUSIONS`, `MVAL_FOODSTUFFS`, `MVAF_FOODSTUFFS`, `MVAF_LOW_VALUE_GOODS`, `NORGES_BANK_RATES` (all W), and `HS_VOEC_EXCLUDED_CLASSES` (I).

## Claims and provenance

All rows were retrieved on 2026-10-16.

| Claim | Source document | Locator | Verbatim quote | Class |
|---|---|---|---|---|
| Foodstuffs, excise goods, and restricted goods are excluded from VOEC | Skatteetaten, Guidelines for VAT On Electronic Commerce (VOEC), `SKE_VOEC_GUIDELINES_URL`, modified 2025-03-28 | §3 "VOEC scheme – key features", p.5 | "The VOEC scheme includes all goods, except: Foodstuffs, which are any goods meant for human consumption, including nutritional and dietary supplements that are not medicinal drugs. Importation of medicinal drugs is restricted / Goods subject to excise duties, including tobacco products and alcoholic beverages. […] / Restricted or illegal goods according to Norwegian law." | W |
| Same exclusion in law | Lovdata, merverdiavgiftsloven, `MVAL_URL`, sist endret 2026-07-01 | § 3-1 (2) | "Det skal også beregnes merverdiavgift ved levering av varer med lav verdi som innføres til andre mottakere enn næringsdrivende og offentlig virksomhet i merverdiavgiftsområdet. Dette gjelder likevel ikke næringsmidler, varer som krever særskilt tillatelse for innførsel eller varer som ilegges særavgifter." | W |
| Same exclusion, Tolletaten's examples | Tolletaten, Om VOEC-ordningen, `TOLL_VOEC_PAGE_URL`, oppdatert 27.11.2025 | "Varer som er omfattet av VOEC-ordningen" | "Følgende varer er ikke omfattet av VOEC: Næringsmidler (for eksempel mat, drikke, kosttilskudd, vitaminer). Varer med restriksjoner (for eksempel legemidler, våpen, alkohol, tobakk). Varer med særavgifter (for eksempel sukker, drikkevareemballasje smøreoljer, hvitevarer med klimagass)." | W |
| Food includes beverages, supplements, and vitamins | Tolletaten, Om VOEC-ordningen, `TOLL_VOEC_PAGE_URL` | as above | "Næringsmidler (for eksempel mat, drikke, kosttilskudd, vitaminer)." | W |
| Food is any good for human consumption, including drink | Lovdata, merverdiavgiftsloven, `MVAL_URL` | § 5-2 (2) and (3) | "Som næringsmiddel anses enhver mat- eller drikkevare og enhver annen vare som er bestemt til å konsumeres av mennesker." / "Som næringsmiddel anses ikke legemidler, tobakkvarer, alkoholholdige drikkevarer og vann fra vannverk." | W |
| Food is judged by fitness for and sale to human consumption | Lovdata, merverdiavgiftsforskriften, `MVAF_URL`, sist endret 2026-07-01 | § 5-2-1 (1) | "Varer anses som næringsmidler dersom de har en kvalitet som gjør at de er egnet til å konsumeres av mennesker og de omsettes til slikt konsum." | W |
| HS chapters and headings approximate the exclusions | Tolletaten open data, Tolltariff struktur, `TOLLTARIFF_STRUCTURE_URL`, last modified 2026-06-23 | chapter and heading `beskrivelse` fields, see HS classifier table | heading texts as quoted in the HS classifier table; no source maps HS codes to the VOEC exclusions | I |
| The NOK 3,000 limit applies per item | Skatteetaten, VOEC guidelines, `SKE_VOEC_GUIDELINES_URL` | §4 "More on the term 'low value goods'", p.6 | "The less than NOK 3,000 threshold is applied per item – not per consignment. The value of the item at "point of sale" is decisive." | W |
| Same, Tolletaten | Tolletaten, Om VOEC-ordningen, `TOLL_VOEC_PAGE_URL` | "Varer som er omfattet av VOEC-ordningen" | "Varer med lav verdi er fysiske varer verdsatt til 2.999 kroner eller mindre. Verdigrensen gjelder per vare, […] så lenge hver vare har en verdi under 3000 kroner." | W |
| Shipping and insurance are excluded from the item value | Lovdata, merverdiavgiftsforskriften, `MVAF_URL` | § 1-3-8 (1) | "Med vare med lav verdi menes vare med verdi under 3000 kroner. Transport- og forsikringskostnader inngår ikke ved fastsettelse av varens verdi." | W |
| Same, guidelines | Skatteetaten, VOEC guidelines, `SKE_VOEC_GUIDELINES_URL` | §4, p.6 | "Additional costs and fees – e.g. shipping and insurance costs – are excluded when determining if the value is within the NOK 3,000 threshold (but to be included when calculating the VAT, […])." | W |
| Conversion uses a Norges Bank, Tolletaten, or market rate published within 30 days | Lovdata, merverdiavgiftsforskriften, `MVAF_URL` | § 1-3-8 (2)-(3) | "Ved omregning av vareverdien til norske kroner skal det benyttes valutakurs som er publisert av a. tolletaten på toll.no, b. Norges Bank eller en utenlandsk sentralbank, c. aktør som offentlig publiserer spotkurser." / "Valutakursen som benyttes, må ha blitt publisert senest 30 dager før betalingen blir akseptert, […]. Valget av valutakurs må være konsekvent." | W |
| Exchange rates used by the plugin | Norges Bank, EXR dataset, `NORGES_BANK_EXR_URL` | series B.{SEK,EUR,DKK,USD}.NOK.SP, TIME_PERIOD 2026-10-15 | SEK 95.31 (per 100), EUR 10.652, DKK 142.5 (per 100), USD 9.5039 | W |
| Mixed baskets must be split, or the whole shipment taxed at the border | Skatteetaten, VOEC guidelines, `SKE_VOEC_GUIDELINES_URL` | §4.1 "Low value goods – multiple goods in one order – bundling", p.7 | "if a supply of multiple goods consists of one or more goods valued above the NOK 3,000 threshold, or one or more goods that fall outside of the VOEC scheme (e.g. foodstuffs or restricted goods), the consignment must be split into separate consignments in order to avoid ordinary customs declaration of the low value goods." / "the supplier can choose not to charge VAT for the item(s) within the VOEC scheme and make the whole shipment subject to border taxation." | W |
| VOEC covers B2C supplies only | Skatteetaten, VOEC guidelines, `SKE_VOEC_GUIDELINES_URL` | §10.1, p.13 | "Only supplies to private individuals and non-business customers (B2C) can be calculated and reported via the VOEC scheme. […] For B2B-supplies, the recipient is liable to calculate and pay VAT." | W |
| A business buyer is not charged VOEC VAT | Skatteetaten, Guide for sellers in the VOEC scheme – how to treat B2B sales, `SKE_VOEC_B2B_URL`, 2026-02-04 | slide 1 | "The VOEC scheme is only for sales to consumers (B2C) - you cannot sell to businesses in the VOEC scheme" / "If a buyer claims to be a business, they should not be charged with VAT from the seller." | W |
| A business buyer's organisation number has nine digits starting with 8 or 9 | Skatteetaten, B2B guide, `SKE_VOEC_B2B_URL` | slide 1 | "The Norwegian business should provide their organisation number / business identification number. This has nine digits, starting with 8 or 9." | W |

## Contradictions and corrections

The user's first pointer was the third-party FAQ at <https://www.voecnorway.com/faq>, which reads (question 3, retrieved 2026-10-16): "Certain items are excluded, including alcohol, tobacco, high-value goods (over NOK 3,000), firearms, certain food items, pharmaceuticals, and other regulated goods."
The official sources exclude all foodstuffs, not certain food items: the guidelines §3 ("Foodstuffs, which are any goods meant for human consumption"), mval § 3-1 (2) ("næringsmidler"), and Tolletaten ("Næringsmidler (for eksempel mat, drikke, kosttilskudd, vitaminer)").
The plugin follows the official sources and does not cite the FAQ.

The guidelines' appendix "Examples of foodstuffs, restricted goods and goods subject to excise duties in Norway" (p.18), written for the 1 January 2020 change, lists "Non-alcoholic beverages" and "Chocolate and sugar products" as excise goods.
Lovdata's særavgiftsforskriften (FOR-2001-12-11-1451, sist endret FOR-2026-06-23-1247, retrieved 2026-10-16) shows both duties abolished: "Kap. 3-17. (Opphevet) […] kapittel 3-17 opphevet ved forskrift 16 des 2020 nr. 2904 (i kraft 1 jan 2021)" (chocolate and sugar products) and "Kap. 3-4. (Opphevet) […] Kapitlet opphevet ved forskrift 23 juni 2021 nr. 2189 (i kraft 1 juli 2021)" (non-alcoholic beverages).
Kap. 3-16 "Avgift på sukker mv." remains in force, which matches Tolletaten's current example "sukker".
Neither change affects the classifier, because non-alcoholic beverages, chocolate, and sugar are foodstuffs and excluded on that ground.
Tolletaten's current excise examples (sugar, beverage packaging, lubricating oils, white goods with climate gas) go beyond the guidelines' §3 examples (tobacco, alcohol); the classifier covers only alcohol and tobacco, as stated above.

`docs/concepts/scope.md` cites the March 2024 guidelines (`voec-guidelines-mars-2024.pdf`, still served on 2026-10-16) for the split prohibition; the 2025-03-28 guidelines carry the same sentence in §4.1 p.7, "Any unbundling or separation of goods that are offered and sold as one unit to avoid passing the value limit of the VOEC scheme is prohibited."

## Risks and trade-offs

- [An unlabelled or mislabelled commodity escapes the classifier] → accepted; the advisory is a reminder, and description matching would raise false positives on goods such as "chocolate-coloured scarf".
- [Accepted false positives in headings 1211 and 1301] → the message names the item and its class, so the shipper can dismiss it.
- [Static rates drift] → the 5 % margin and the dated `details.rate_date`; a refresh is a data change.
- [A recipient tax id stored for a consumer] → one non-blocking warning.
- [Svalbard and Jan Mayen] → mval § 1-2 (2) places them outside the VAT area, so VOEC does not apply there, yet `lane.to_norway` includes them; see Open questions.

## Open questions

- Should live animals (chapter 01), plants (chapter 06), and seeds for sowing (heading 1209), which the guidelines' appendix lists as restricted goods, form a fourth restricted class in this change, or stay unclassified as specified?
- Should the three rules stay silent for Svalbard and Jan Mayen postal codes (8099, 9170-9179, the ranges `exclusions.py` already uses), where Norwegian VAT and VOEC do not apply?
- Should the README Requirements at a glance matrix gain VOEC cells in its Norway column, or should the three advisories appear only in the Across carriers summary line, as `zero_value_line` and `ch_discount_on_invoice` do?
- The main specification's answering-procedures requirement omits the six country-requirement codes added by `dhl-country-specific-requirements`, which `procedures.ANSWERING` maps to the empty set; this delta keeps that omission and adds only the three VOEC codes.
