"""Sources cited by the Nordic conventions advisories.

Each ``Source`` carries the evidence tag of the karrio fork's facts note
``docs/notes/customs/nordic-trade-documents-facts.md`` (branch
``docs-openspec``, commit baf8eb3dd), cited as FN with line numbers: S is
repository code or a vendored or cited carrier API specification, W is public
carrier or authority documentation, and I is inference. Connector behaviour is cited from the
standalone connectors: karrio-postnord's README and code at commit
320f3ad4f118f406e7b68ff7d4adeaca35b1d893, and karrio-dhl-freight-sweden's
README and docs pages at commit 7a2214d and the commits that introduced its
refusals.
"""

import typing

import attr

EVIDENCE_TAGS = ("S", "W", "I")

FACTS_NOTE = "karrio fork docs/notes/customs/nordic-trade-documents-facts.md@baf8eb3dd"

PN_SE_EN_PAGE = "https://web.archive.org/web/20260116090151/https://www.postnord.se/en/business/import-export-customs/customs-documents-and-shipping-documents/"
PN_SE_SV_PAGE = "https://www.postnord.se/foretag/import-export-tull/tulldokument-och-frakthandlingar-for-foretag/ (Wayback 2026-02-08)"
PN_SE_POSTPAKET_TERMS_URL = "https://api2.postnord.com/rest/customer/v2/ptm/file/download/5341.28764?disposition=inline (valid 2025-05-02)"
PN_SE_SERVICE_POINT_TERMS_URL = "https://www.avropa.se/globalassets/bilagor/1.-aktuella-rao/postformedlingstjanster-2021/paketformedlingstjanster--1-lev-postnord/sarskilda-villkor-service-point-2026.pdf (valid 2026-01-01)"
PN_FI_PAGE_URL = "https://www.postnord.fi/en/sending/online-tools/customs-information/ (read 2026-09-25)"
PN_FI_TERMS = "PostNord FI special terms for parcels, valid 2026-05-01 (Wayback 2026-06-10)"
PN_DK_PAGE_URL = "https://www.postnord.dk/erhverv/eksport/ (Wayback 2026-03-10)"
DHL_MAN_URL = "https://dhlpaket.se/dashboard/specifications/products/ (product manual v5.26, updated 2026-10-01, valid from 2026-11-01, sha256 050660c37ba93d1ae9514c50dfa42c2010bc87763ccaff51a740b2526af11b73)"
DHL_CIE_URL = "https://www.dhl.com/content/dam/dhl/local/se/dhl-freight/documents/pdf/se-freight-customs-information-export-en.pdf (2025-02-03)"
DHL_PRL_URL = "https://www.dhl.com/content/dam/dhl/local/se/dhl-freight/documents/pdf/se-freight-price-list-additional-services-sv.pdf (valid 2026-05-01)"
DHL_API_FARM_URL = "https://dhlpaket.se/dashboard/services/api-farm/ (registration required, read 2026-08-11)"
DHL_CSR_URL = "https://www.dhl.com/se-en/home/freight/help-center-for-european-road-and-rail/useful-information-and-downloads.html (Country-specific shipping requirements (English), accessed 2026-10-09)"
BRING_URL = "https://www.bring.se/tjanster/tull/tulldokument"
BAZG_R_69_03_URL = "https://www.bazg.admin.ch/dam/de/sd-web/mIvoM5CF7ydH/steuerbemessungsgrundlage-de.pdf (valid 2025-01-01)"
PN_SE_NO_PAGE_URL = "https://www.postnord.se/privat/skicka/skicka-brev-och-paket-utomlands/skicka-paket-till-norge/ (read 2026-10-02)"
TV_EXPORT_DOCUMENTS_URL = "https://www.tullverket.se/sv/foretag/exporteravaror/deklareravarorvidexport/styrkandehandlingarvidexport.4.78aa922815794d801e25e3.html (updated 2026-06-12, read 2026-10-02)"
DHL_EXPRESS_CUSTOMS_URL = "https://mydhl.express.dhl/content/dam/downloads/global/en/customs-guide/express_global_customs_customer_guidelines.pdf.coredownload.pdf"
DHL_CONNECTOR_README_URL = "https://github.com/PrimePack-AB/karrio-dhl-freight-sweden/blob/7a2214d/README.md (read 2026-10-08)"
DHL_CONNECTOR_DESTINATIONS_URL = "https://github.com/PrimePack-AB/karrio-dhl-freight-sweden/blob/7a2214d/docs/concepts/destinations.md (read 2026-10-08)"
DHL_CONNECTOR_TERRITORY_CHECK = "https://github.com/PrimePack-AB/karrio-dhl-freight-sweden/commit/142b62d5d48a1ba40cbddd8a46be7ec2c0442b0a (committed 2026-10-08)"
DHL_CONNECTOR_JOINT_DECLARATION_CHECK = "https://github.com/PrimePack-AB/karrio-dhl-freight-sweden/commit/f86c8ac11fd9b017d4eb2a77bbf06fa88a1fa3fb (committed 2026-10-08)"
DHL_CONNECTOR_COMMERCIAL_INVOICE_CHECK = "https://github.com/PrimePack-AB/karrio-dhl-freight-sweden/commit/ec180e61ca7ae4e763f58d9919ad9be0ae2ab56f (committed 2026-10-06)"
PN_CONNECTOR_README_URL = "https://github.com/PrimePack-AB/karrio-postnord/blob/320f3ad4f118f406e7b68ff7d4adeaca35b1d893/README.md (read 2026-10-19)"
SKE_VOEC_GUIDELINES_URL = "https://www.skatteetaten.no/globalassets/bedrift-og-organisasjon/voec/sell-charge-and-ship-goods-to-norway.pdf (PDF modified 2025-03-28, read 2026-10-16)"
SKE_VOEC_B2B_URL = "https://www.skatteetaten.no/globalassets/bedrift-og-organisasjon/voec/how-to-treat-b2b-sales-2026.pdf (PDF created 2026-02-04, read 2026-10-16)"
TOLL_VOEC_PAGE_URL = "https://www.toll.no/no/bedrift/import/voec/om-voec-ordningen (oppdatert 2025-11-27, read 2026-10-16)"
MVAL_URL = "https://lovdata.no/dokument/NL/lov/2009-06-19-58 (LOV-2009-06-19-58, sist endret LOV-2025-12-22-121 fra 2026-07-01, read 2026-10-16)"
MVAF_URL = "https://lovdata.no/dokument/SF/forskrift/2009-12-15-1540 (FOR-2009-12-15-1540, sist endret FOR-2026-06-26-1398 fra 2026-07-01, read 2026-10-16)"
TOLLTARIFF_STRUCTURE_URL = "https://data.toll.no/dataset/6350e783-b989-4c7c-9ec0-de2dcb97363c/resource/68f78255-cbb0-4e75-86b1-3d5928816903/download/tolltariffstruktur.json (version 1.5, last modified 2026-06-23, read 2026-10-16)"
NORGES_BANK_EXR_URL = "https://data.norges-bank.no/api/data/EXR/B.EUR+SEK+DKK+USD.NOK.SP?format=csv&lastNObservations=1&locale=en (rates for 2026-10-15, read 2026-10-16)"
BRING_POSTAL_CODE_REGISTER_URL = "https://www.bring.no/postnummerregister-ansi.txt (described at https://www.bring.no/tjenester/adressetjenester/postnummer/postnummertabeller-veiledning, read 2026-10-16; the file carries no date of its own)"


@attr.s(auto_attribs=True, frozen=True)
class Source:
    """One cited document or code location with its evidence tag."""

    tag: str
    reference: str
    statement: str

    def to_dict(self) -> dict:
        return attr.asdict(self)


def _ref(lines: str, location: str) -> str:
    return f"{lines}; {location}"


# PostNord Sweden

PN_SE_SERVICE_POINT_TERMS_PAPER = Source(
    "W",
    _ref("FN:118-119", PN_SE_SERVICE_POINT_TERMS_URL),
    "Service Point special terms §4: a commercial invoice \"in at least two copies in English shall accompany the parcel\", in a plastic pocket on parcel no. 1; digital data prevails over paper on discrepancy.",
)
PN_SE_SERVICE_POINT_TERMS_NORWAY = Source(
    "W",
    _ref("FN:118", PN_SE_SERVICE_POINT_TERMS_URL),
    "Service Point special terms §4: \"To Norway the commercial invoice and shipment list shall be sent digitally\".",
)
PN_SE_EN_PAGE_PARCEL_TRIPLICATE = Source(
    "W",
    _ref("FN:100, FN:142", PN_SE_EN_PAGE),
    "English customs documents page: Service Point, MyPack Home, Pallet, and Parcel need an invoice, not CN22/CN23; shipping document and invoice \"in triplicate\" (3 copies).",
)
PN_SE_SV_PAGE_PARCEL_TWO_COPIES = Source(
    "W",
    _ref("FN:142, FN:264", PN_SE_SV_PAGE),
    "Swedish customs documents page: the invoice in \"två exemplar\" (2 copies).",
)
PN_SE_PLASTIC_POCKET_ORIGIN = Source(
    "I",
    _ref("FN:148", FACTS_NOTE),
    "Neither 2026 PostNord SE web snapshot contains the plastic-pocket wording for invoices; that wording comes from the Service Point special terms.",
)
PN_SE_NORWAY_CHANNELS = Source(
    "W",
    _ref("FN:142, FN:147", PN_SE_SV_PAGE),
    "Swedish customs documents page: to Norway the invoice goes digitally, not with the parcel, through the Booking API, PostNord Skicka Direkt Business, foravisering.export@postnord.com, or upload in MyCustoms, where shippers can \"förse oss med tullinformation, eller ladda upp en tullfaktura\".",
)
PN_SE_NORWAY_ONLY_CHANNELS = Source(
    "W",
    _ref("FN:149", PN_SE_SV_PAGE),
    "None of the PostNord SE separate invoice channels is stated to apply to destinations other than Norway.",
)
PN_SE_SV_PAGE_NORWAY_LETTERS = Source(
    "W",
    _ref("FN:99, FN:108", PN_SE_SV_PAGE),
    "Swedish customs documents page, letters: \"OBS! Vid export till Norge behöver Handelsfaktura och VOEC* anges från 0 kr.\"",
)
PN_CONNECTOR_PARCEL_CUSTOMS_INVOICE = Source(
    "S",
    _ref(
        "Customs declarations, At booking, L158, L162",
        f"{PN_CONNECTOR_README_URL}; karrio/providers/postnord/units.py L499-L507 (customs_structure)",
    ),
    "PostNord connector README: \"When a shipment carries `customs` with at least one commodity, the booking embeds one customs structure selected by the service.\" and \"every other service is a parcel product and sends a customs invoice (`customsInvoice`)\".",
)
PN_CONNECTOR_INTERNATIONAL_PARCEL_CN23 = Source(
    "S",
    _ref(
        "Customs declarations, At booking, L162-L164, L208, L212, L219",
        f"{PN_CONNECTOR_README_URL}; karrio/providers/postnord/units.py L499-L507 (customs_structure), shipment/create.py L29-L38, L123-L148, and L194-L240 (CN23 label check) and L649-L702 (_customs_declaration_cn23)",
    ),
    "PostNord connector README: \"International Parcel (91) sends a CN23 declaration (`customsDeclarationCN23`)\", \"International Parcel (91) books the CN23 unconditionally\", \"Duties after booking, such as printing the customs documents and attaching the invoice copies to the parcel, are the consumer's.\", \"For International Parcel (91), a test-mode sandbox booking carrying the mapper-built CN23 was accepted with `printoutComposition` `{cn23: 1, label: 1}` and one two-page A4 PDF — the parcel label on page 1, the CN23 on page 2\", \"test mode sends no EDI downstream, so production composition may differ\", \"International Parcel (91) labels are verified on PDF against the CN23 page-text markers seeded from that capture\", \"a ZPL label skips the check, no ZPL CN23 printout having been captured\", and \"For letter services and International Parcel (91), no standalone document is fetched unless the `postnord_standalone_customs_documents` opt-in is set\"; the CN23 carries no invoice number, date, or type.",
)
PN_SE_POSTPAKET_TERMS = Source(
    "W",
    _ref("FN:103, FN:111", PN_SE_POSTPAKET_TERMS_URL),
    "Postpaket Utrikes terms §2: CN23 in two copies and a commercial invoice in 2 copies with the parcel when the goods value exceeds SEK 2 000 or the goods are sent for commercial purposes (\"För paket med varuvärde över 2000 kr eller då varan skickas i handelssyfte krävs utöver frakthandling och Exportdeklaration Post CN23, i två exemplar en handelsfaktura i 2 exemplar med paketet.\").",
)
PN_SE_EN_PAGE_POSTPAKET = Source(
    "W",
    _ref("FN:102, FN:107", PN_SE_EN_PAGE),
    "English customs documents page, EMS and Parcel Post International: \"> SEK 2,000: CN23 and commercial or pro forma invoice in triplicate.\" (3 copies, on value only).",
)
PN_SE_SV_PAGE_POSTPAKET = Source(
    "W",
    _ref("FN:102, FN:109", PN_SE_SV_PAGE),
    "Swedish customs documents page, EMS and Postpaket: \"> 2 000 kr: CN23 och handels- eller proformafaktura i tre exemplar.\" (3 copies, on value only).",
)
PN_POSTPAKET_CODE_91 = Source(
    "S",
    _ref("FN:165", "karrio modules/connectors/postnord/karrio/providers/postnord/units.py:146; modules/connectors/postnord/vendor/docs/general-descriptions.pdf"),
    "Code 91 is the contract and EDI product: postnord_postpaket_utrikes = \"91\" matches \"91 Z91 Postpaket Utrikes\" and \"International Parcel(91)\".",
)
PN_POSTPAKET_CODE_95 = Source(
    "W",
    _ref("FN:166", "https://api2.postnord.com/rest/customer/v2/ptm/file/download/5341.28763 (PostNord terms valid 2025-05-02)"),
    "Code 95 is the direct-payment product Parcel Post International (Postpaket Utrikes); its terms require two CN23 copies and three copies of the commercial invoice with the parcel above SEK 2 000 or for commercial purposes.",
)
PN_POSTPAKET_TERMS_PROFORMA = Source(
    "W",
    _ref("FN:111, FN:113", PN_SE_POSTPAKET_TERMS_URL),
    "Postpaket Utrikes terms §2: \"Proformafaktura … får endast användas vid gåva eller varuprov.\"",
)

# PostNord Finland

PN_FI_WEB_PAGE = Source(
    "W",
    _ref("FN:143, FN:152", PN_FI_PAGE_URL),
    "postnord.fi customs information: \"If necessary, the invoice can be attached to the shipment or submitted separately to support customs clearance. A copy of the invoice can be sent by email to address tullaus.fi@postnord.com [...]. Original invoices must be prepared in English and signed by hand if necessary\".",
)
PN_FI_WEB_PAGE_NORWAY = Source(
    "W",
    _ref("FN:153", PN_FI_PAGE_URL),
    "postnord.fi customs information: for Norway the electronic customs data must arrive before the shipment.",
)
PN_FI_SPECIAL_TERMS = Source(
    "W",
    _ref("FN:143, FN:154", PN_FI_TERMS),
    "PostNord FI special terms for parcels: non-EU parcels require \"a signed commercial invoice in English in triplicate\", and invoices to Norway are electronic; EDI prevails over the shipping document on discrepancy.",
)
PN_FI_GOVERNING_UNRESOLVED = Source(
    "I",
    _ref("FN:155, FN:267", FACTS_NOTE),
    "The web page appears relaxed after December 2025 while the contract terms were not; which of the two governs is unresolved.",
)

# PostNord Denmark

PN_DK_EXPORT_PAGE = Source(
    "W",
    _ref("FN:144, FN:157", PN_DK_PAGE_URL),
    "postnord.dk export: documents in a plastic pocket visible on the parcel; Norway 2 invoices, Switzerland and Liechtenstein 3, Great Britain 2, rest of world 1 CN23 and 2 invoices, the invoice \"not required\" but recommended; a lodged export declaration is copied to eksport@postnord.com.",
)

# DHL Freight Sweden

DHL_CONNECTOR_CUSTOMS_SERVICES_OPT_IN = Source(
    "S",
    _ref("Customs services", DHL_CONNECTOR_README_URL),
    "DHL Freight Sweden connector README: \"The manual offers four customs services, and the connector sends none unless an option selects it; each carries a DHL fee, and the manual allows only one per shipment.\"",
)
DHL_MAN_CUSTOMS_SELECTION = Source(
    "W",
    _ref("FN:196", f"{DHL_MAN_URL} §7.6.1 p.163, §6.7 p.96"),
    "Customs handling (Standard or Full service) or own declaration must be selected for CH, GB, NO, Åland (FI 22) and other non-EU destinations.",
)
DHL_MAN_JOINT_DECLARATION = Source(
    "W",
    _ref("Product manual v5.26", f"{DHL_MAN_URL} §6.8 p.98"),
    "Customs, joint declaration: valid country NO; needs a separate agreement; cannot be combined with the other customs services.",
)
DHL_CONNECTOR_JOINT_DECLARATION_DESTINATIONS = Source(
    "S",
    _ref("Customs services", DHL_CONNECTOR_README_URL),
    "The DHL Freight Sweden connector's customs table names NO and CH for the joint declaration (dhl_freight_sweden_customs_joint_declaration), the manual naming NO only, because product matches on its sandbox account list customsJointDeclaration to NO and CH; from karrio-dhl-freight-sweden commit https://github.com/PrimePack-AB/karrio-dhl-freight-sweden/commit/f86c8ac11fd9b017d4eb2a77bbf06fa88a1fa3fb the connector refuses the joint declaration to other recipient countries across the EU VAT area border (JOINT_DECLARATION_COUNTRIES).",
)
DHL_CONNECTOR_ALAND_CUSTOMS = Source(
    "S",
    _ref("Åland", DHL_CONNECTOR_DESTINATIONS_URL),
    "DHL Freight Sweden connector sandbox evidence: from SE to FI 22100, Parcel Connect Plus (112) was rejected with 24003 \"not available for this country combination\" with customs handling full service and with Standard, although the manual lists Åland for Standard (§6.6 p94), and Parcel Connect (109) was booked with customs data and no customs service (booking 2906762592), showing that DHL stored the customs data, not how DHL clears it; the connector refuses full service and Standard to or from FI 22000-22999, also under AX.",
)
DHL_PRL_NO_FEE_FREE_MODE = Source(
    "W",
    _ref("FN:208", DHL_PRL_URL),
    "No fee-free customs mode exists for non-EU destinations.",
)
DHL_OWN_DECLARATION_FEE_INFERENCE = Source(
    "I",
    _ref("FN:208, FN:269", FACTS_NOTE),
    "The price list has no own-declaration line for 109 and 112, so whether DHL bills own declaration on them is inferred, not stated.",
)
DHL_MAN_INVOICE_COPY = Source(
    "W",
    _ref("FN:213", f"{DHL_MAN_URL} §7.6.2 p.163"),
    "\"A copy of the invoice must still be sent\" even with complete EDI data under standard customs handling.",
)
DHL_CIE_INVOICE_ROUTES = Source(
    "W",
    _ref("FN:214", f"{DHL_CIE_URL} p.9"),
    "The invoice copy is emailed to dhlfreight.int.se@dhl.com shortly after booking, or uploaded in myDHL Freight, one document per shipment with a clear reference.",
)
DHL_CIE_REMINDER_FEES = Source(
    "W",
    _ref("FN:216", f"{DHL_CIE_URL} p.12; {DHL_PRL_URL}"),
    "Missing documents stop the shipment, with reminder fees of 390 kr (650 kr for Great Britain).",
)
DHL_API_NO_UPLOAD = Source(
    "S",
    _ref(
        "FN:179",
        f"{DHL_API_FARM_URL}; all 13 API Farm specifications, version 2.10.0; "
        "TransportInstruction 2.10.0 and Print API 2.10.0 for the booking flow",
    ),
    "The DHL Freight Sweden API has no attachment or upload endpoint.",
)
DHL_MAN_OUTSIDE_COPIES = Source(
    "W",
    _ref("FN:215", f"{DHL_MAN_URL} §5.14 p.62"),
    "For Parcel Connect (109): \"Two copies of customs documents must also be attached on the outside of the package\".",
)
DHL_OUTSIDE_COPIES_UNCONFIRMED = Source(
    "I",
    _ref("FN:215, FN:268", FACTS_NOTE),
    "Whether Parcel Connect Plus (112) and road-freight products require copies attached to the outside of the package is unconfirmed.",
)
DHL_CONNECTOR_VOEC_SERVICE = Source(
    "S",
    _ref("Customs services", DHL_CONNECTOR_README_URL),
    "DHL Freight Sweden connector README: \"VOEC (VAT on e-commerce, NO) is sent from `customs.options.voec_number` and has not been booked in the sandbox.\"",
)
DHL_MAN_VOEC_MARKING = Source(
    "W",
    _ref("FN:217", f"{DHL_MAN_URL} §6.5 p.92, §6.6 p.94, §9.4.2 p.168"),
    "The Norway VOEC ID must be printed on the package or label.",
)
DHL_MAN_VOEC_PARCEL_CONNECT = Source(
    "W",
    _ref("FN:206", f"{DHL_MAN_URL} §6.5 p.92, §6.6 p.94"),
    "The voecSupplyVAT service is VOEC with Parcel Connect (109) to Norway, sent in the API as additionalServices.voecSupplyVAT.vatId.",
)
DHL_CSR_CYPRUS_DOCUMENTS = Source(
    "W",
    _ref("Cyprus", DHL_CSR_URL),
    "Country-specific requirements for Cyprus: a commercial invoice and packing list are required to prove the Union status of the goods, a T2L document where applicable, copies of the recipient's ID documents, front and back, when the recipient is a private individual, and the documents can be uploaded in myDHL Freight.",
)
DHL_CSR_GREEK_TAX_IDS = Source(
    "W",
    _ref("Greece", DHL_CSR_URL),
    "Country-specific requirements for Greece: the sender's and the recipient's VAT numbers are required, and EL000000000 can be used for a private individual.",
)
DHL_CSR_SPAIN_DG_DOCUMENTS = Source(
    "W",
    _ref("Spain", DHL_CSR_URL),
    "Country-specific requirements for Spain: dangerous goods shipments to and from Spain must carry both a dangerous goods declaration and a material safety data sheet, which can be uploaded in myDHL Freight.",
)
DHL_MAN_GREEK_TAX_ID_PRODUCTS = Source(
    "W",
    _ref("Product manual v5.26", f"{DHL_MAN_URL} §5.4 p.22, §5.11 p.51, §5.19 p.81"),
    "The shipment information of Road Freight Standard (202), SPI, and Home Delivery International (601) makes a VAT number or TIN mandatory for all parties on shipments to and from Greece.",
)
DHL_CONNECTOR_GREEK_TAX_ID_PRODUCTS = Source(
    "S",
    _ref("Inside the EU VAT area", DHL_CONNECTOR_README_URL),
    "The connector refuses 202, SPI, or 601 to or from GR without a VAT number or TIN for both parties (PartyTaxIdError), reading each party's tax id from federal_tax_id or state_tax_id; the product set is PARTY_TAX_ID_PRODUCTS in its units.py.",
)
DHL_CONNECTOR_TRANSPORT_DECLARATION_PRODUCTS = Source(
    "S",
    _ref("Inside the EU VAT area", DHL_CONNECTOR_README_URL),
    "Inside the EU VAT area the connector carries a transport declaration on three lanes: SENT to or from PL, and EKAER and UIT to or from HU and RO, on TRANSPORT_DECLARATION_PRODUCTS (202, 205, 233, SPI, and 601) in its units.py.",
)
DHL_CONNECTOR_TRANSPORT_DECLARATION_DEFAULTS = Source(
    "S",
    _ref("Inside the EU VAT area", DHL_CONNECTOR_README_URL),
    "Without a declaration option the connector declares SENT free, declares EKAER or UIT free below 500 kg total gross weight (TRANSPORT_DECLARATION_FREE_WEIGHT_LIMIT_KG), refuses an undeclared EKAER or UIT shipment at or above, and fails a missing or contradictory declaration with SentInformationError or TransportDeclarationError; weight is the only criterion it checks.",
)

# Invoice type

PN_CONNECTOR_COMMERCIAL_FLAG = Source(
    "S",
    _ref(
        "Customs declarations, At booking, L190",
        f"{PN_CONNECTOR_README_URL}; karrio/providers/postnord/shipment/create.py L837-L841",
    ),
    "PostNord connector README, customs invoice mapping: \"`customs.commercial_invoice` | `type`: `COMMERCIAL` when true, `PROFORMA` when false or omitted\".",
)
DHL_CONNECTOR_COMMERCIAL_FLAG = Source(
    "S",
    _ref("Commercial or proforma invoice", DHL_CONNECTOR_README_URL),
    "DHL Freight Sweden connector README: \"True sends a `CommercialInvoice` document, and false or unset sends a `ProformaInvoice`.\" and \"Outside the EU VAT area, content counts as a sale unless `customs.content_type` is `documents`, `gift`, `return_merchandise`, or `sample`, and a sale without `customs.commercial_invoice` true fails with `CommercialInvoiceRequiredError`.\"",
)
DHL_CONNECTOR_COMMERCIAL_INVOICE_REQUIRED = Source(
    "S",
    _ref("CommercialInvoiceRequiredError", DHL_CONNECTOR_COMMERCIAL_INVOICE_CHECK),
    "Across the EU VAT area border the DHL Freight Sweden connector refuses a booking with customs data whose content is sale-like, a customs.content_type other than documents, gift, return_merchandise, or sample, or none, and whose customs.commercial_invoice is not true, with CommercialInvoiceRequiredError before sending it; inside the area it drops customs data with a warning instead.",
)
PROFORMA_FOR_GOODS_NOT_SOLD = Source(
    "W",
    _ref("FN:56", f"{BRING_URL}; {DHL_CIE_URL} p.5"),
    "The commercial invoice has no fixed format; a proforma invoice is used for goods not sold and states \"No charge. Value for customs purposes only\".",
)

# Customs values

BAZG_RABATTE = Source(
    "W",
    _ref("§5.5.3", BAZG_R_69_03_URL),
    "BAZG Richtlinie R-69-03 §5.5.3 \"Rabatte\": discounts are not part of the taxable consideration, and an item the supplier hands over with a sold item as a discount in kind or add-on (Zugabe) is not taxed additionally on import, provided it is directly connected to the supply causing the import.",
)
PN_SE_NO_PAGE_NON_ZERO_VALUE = Source(
    "W",
    _ref("Skicka paket till Norge", PN_SE_NO_PAGE_URL),
    "PostNord SE page on parcels to Norway: \"värdet på en handels- eller proformafaktura får aldrig vara 0 kronor. Allt har ett värde även om innehållet är en gåva eller ett varuprov.\"",
)
TV_PROFORMA_NON_ZERO_VALUE = Source(
    "W",
    _ref("Styrkande handlingar vid export", TV_EXPORT_DOCUMENTS_URL),
    "Tullverket, supporting documents for export: a pro forma invoice states \"värde för tulländamål för varje varuslag (får inte vara 0 kronor)\" and \"No charge. Value for customs purposes only.\", and an invoice states \"eventuella rabatter och vilken typ av rabatter\".",
)
DHL_EXPRESS_NO_ZERO_VALUES = Source(
    "W",
    _ref("Customs customer guidelines", DHL_EXPRESS_CUSTOMS_URL),
    "DHL Express customs guidelines: \"zero (0) values are not acceptable\" for line values, and invoice values must comply with WTO valuation rules.",
)
DHL_MAN_PRODUCT_LANES = Source(
    "W",
    _ref("Product manual v5.26", f"{DHL_MAN_URL} §5.1 p.13, §5.2 p.15 to §5.19 p.82, §5.15 p.65"),
    "DHL Freight Sweden product manual v5.26: the overview classifies Paket (102), Service Point B2C (103) and C2B (104), Hemleverans Paket (118), Special (209), Pall (210), Stycke (211), Parti (212), Home Delivery (401), and Home Delivery Return (402, 502) as domestic, and Parcel Return Connect (107), Parcel Connect (109), Parcel Connect Plus (112), Road Freight Standard (202), Road Freight Direct (205), Road Freight Priority (233), Standard Pallet International (SPI), and Home Delivery International B2C (601) as international; each product's \"Valid countries\" table lists its countries, SE alone for the domestic products; 202, 205, 233, SPI, and 601 \"can be used to and from Sweden\"; 107 \"can only be used when a DHL PARCEL CONNECT (109) shipment is to be returned to the original sender\".",
)
DHL_MAN_EXCLUDED_AREAS = Source(
    "W",
    _ref("Product manual v5.26", f"{DHL_MAN_URL} §5.3 p.18, §5.4 p.23, §5.9 p.43, §5.11 p.52, §5.14 p.63, §5.15 p.66"),
    "DHL Freight Sweden product manual v5.26 \"Excluded regions/areas\": postal codes Parcel Connect Plus (112), Parcel Connect (109), and Parcel Return Connect (107, from the listed countries) do not serve in DK, ES, FR, IT, NO, and PT, Jersey, Guernsey, and Northern Ireland under GB, and the Caribbean Netherlands; Road Freight Standard (202), Road Freight Direct (205), and SPI exclude UA 95000-99999.",
)
DHL_CONNECTOR_EXCLUDED_POSTAL_CODES = Source(
    "S",
    _ref("Excluded postal codes", DHL_CONNECTOR_DESTINATIONS_URL),
    "The DHL Freight Sweden connector refuses a booking whose shipper or recipient postal code a product excludes, after mapping territory codes to their parent, with ExcludedDestinationError; for 202, 233, and 601 it applies the Product API catalog's postalCodeExcludes quoted from product matches answers.",
)
DHL_CONNECTOR_TERRITORY_POSTAL_CODES = Source(
    "S",
    _ref("TerritoryPostalCodeError", DHL_CONNECTOR_TERRITORY_CHECK),
    "The DHL Freight Sweden connector refuses a shipper or recipient with the country code AX, IC, EA, FO, or GL whose postal code is missing or, normalised under the parent, lies outside the territory (FI 22000-22999; ES 35000-35999 or 38000-38999; ES 51000-51999 or 52000-52999; DK 3800-3999 or three digits; DK 3800-3999), because such a code would otherwise be booked as the parent's mainland, inside the EU VAT area, with its customs data dropped.",
)
DHL_CONNECTOR_JOINT_DECLARATION_DESTINATION = Source(
    "S",
    _ref("JointDeclarationDestinationError", DHL_CONNECTOR_JOINT_DECLARATION_CHECK),
    "Across the EU VAT area border the DHL Freight Sweden connector refuses dhl_freight_sweden_customs_joint_declaration to a recipient country, after the territory mapping, other than NO, the manual's only valid country, and CH, which product matches offer; inside the area it drops customs services with a warning instead.",
)

# VOEC applicability

SKE_VOEC_EXCLUDED_GOODS = Source(
    "W",
    _ref("§3 \"VOEC scheme – key features\" p.5", SKE_VOEC_GUIDELINES_URL),
    "Skatteetaten VOEC guidelines §3: \"The VOEC scheme includes all goods, except: Foodstuffs, which are any goods meant for human consumption, including nutritional and dietary supplements that are not medicinal drugs. Importation of medicinal drugs is restricted / Goods subject to excise duties, including tobacco products and alcoholic beverages. […] / Restricted or illegal goods according to Norwegian law.\"",
)
SKE_VOEC_PER_ITEM_THRESHOLD = Source(
    "W",
    _ref("§4 \"More on the term 'low value goods'\" p.6", SKE_VOEC_GUIDELINES_URL),
    "Skatteetaten VOEC guidelines §4: \"The less than NOK 3,000 threshold is applied per item – not per consignment. The value of the item at \"point of sale\" is decisive.\" / \"Additional costs and fees – e.g. shipping and insurance costs – are excluded when determining if the value is within the NOK 3,000 threshold (but to be included when calculating the VAT, […]).\"",
)
SKE_VOEC_MIXED_CONSIGNMENT = Source(
    "W",
    _ref("§4.1 \"Low value goods – multiple goods in one order – bundling\" p.7", SKE_VOEC_GUIDELINES_URL),
    "Skatteetaten VOEC guidelines §4.1: \"if a supply of multiple goods consists of one or more goods valued above the NOK 3,000 threshold, or one or more goods that fall outside of the VOEC scheme (e.g. foodstuffs or restricted goods), the consignment must be split into separate consignments in order to avoid ordinary customs declaration of the low value goods.\" / \"the supplier can choose not to charge VAT for the item(s) within the VOEC scheme and make the whole shipment subject to border taxation.\"",
)
SKE_VOEC_B2C_ONLY = Source(
    "W",
    _ref("§10.1 p.13", SKE_VOEC_GUIDELINES_URL),
    "Skatteetaten VOEC guidelines §10.1: \"Only supplies to private individuals and non-business customers (B2C) can be calculated and reported via the VOEC scheme. […] For B2B-supplies, the recipient is liable to calculate and pay VAT.\"",
)
SKE_VOEC_B2B = Source(
    "W",
    _ref("slide 1", SKE_VOEC_B2B_URL),
    "Skatteetaten guide for sellers in the VOEC scheme – how to treat B2B sales: \"The VOEC scheme is only for sales to consumers (B2C) - you cannot sell to businesses in the VOEC scheme\" / \"If a buyer claims to be a business, they should not be charged with VAT from the seller.\"",
)
TOLL_VOEC_EXCLUDED_GOODS = Source(
    "W",
    _ref("\"Varer som er omfattet av VOEC-ordningen\"", TOLL_VOEC_PAGE_URL),
    "Tolletaten, Om VOEC-ordningen: \"Følgende varer er ikke omfattet av VOEC: Næringsmidler (for eksempel mat, drikke, kosttilskudd, vitaminer). Varer med restriksjoner (for eksempel legemidler, våpen, alkohol, tobakk). Varer med særavgifter (for eksempel sukker, drikkevareemballasje smøreoljer, hvitevarer med klimagass).\"",
)
TOLL_VOEC_PER_ITEM_THRESHOLD = Source(
    "W",
    _ref("\"Varer som er omfattet av VOEC-ordningen\"", TOLL_VOEC_PAGE_URL),
    "Tolletaten, Om VOEC-ordningen: \"Varer med lav verdi er fysiske varer verdsatt til 2.999 kroner eller mindre. Verdigrensen gjelder per vare, […] så lenge hver vare har en verdi under 3000 kroner.\"",
)
MVAL_LOW_VALUE_EXCLUSIONS = Source(
    "W",
    _ref("§ 3-1 (2)", MVAL_URL),
    "Merverdiavgiftsloven § 3-1 (2): \"Det skal også beregnes merverdiavgift ved levering av varer med lav verdi som innføres til andre mottakere enn næringsdrivende og offentlig virksomhet i merverdiavgiftsområdet. Dette gjelder likevel ikke næringsmidler, varer som krever særskilt tillatelse for innførsel eller varer som ilegges særavgifter.\"",
)
MVAL_FOODSTUFFS = Source(
    "W",
    _ref("§ 5-2 (2) and (3)", MVAL_URL),
    "Merverdiavgiftsloven § 5-2: \"Som næringsmiddel anses enhver mat- eller drikkevare og enhver annen vare som er bestemt til å konsumeres av mennesker.\" / \"Som næringsmiddel anses ikke legemidler, tobakkvarer, alkoholholdige drikkevarer og vann fra vannverk.\"",
)
MVAF_FOODSTUFFS = Source(
    "W",
    _ref("§ 5-2-1 (1)", MVAF_URL),
    "Merverdiavgiftsforskriften § 5-2-1 (1): \"Varer anses som næringsmidler dersom de har en kvalitet som gjør at de er egnet til å konsumeres av mennesker og de omsettes til slikt konsum.\"",
)
MVAF_LOW_VALUE_GOODS = Source(
    "W",
    _ref("§ 1-3-8 (1)-(3)", MVAF_URL),
    "Merverdiavgiftsforskriften § 1-3-8: \"Med vare med lav verdi menes vare med verdi under 3000 kroner. Transport- og forsikringskostnader inngår ikke ved fastsettelse av varens verdi.\" / \"Ved omregning av vareverdien til norske kroner skal det benyttes valutakurs som er publisert av a. tolletaten på toll.no, b. Norges Bank eller en utenlandsk sentralbank, c. aktør som offentlig publiserer spotkurser.\" / \"Valutakursen som benyttes, må ha blitt publisert senest 30 dager før betalingen blir akseptert, […]. Valget av valutakurs må være konsekvent.\"",
)
NORGES_BANK_RATES = Source(
    "W",
    _ref("series B.{SEK,EUR,DKK,USD}.NOK.SP, TIME_PERIOD 2026-10-15", NORGES_BANK_EXR_URL),
    "Norges Bank exchange rates: SEK 95.31 (per 100), EUR 10.652, DKK 142.5 (per 100), USD 9.5039.",
)
SKE_VOEC_RESTRICTED_EXAMPLES = Source(
    "W",
    _ref(
        "Appendix \"Examples of foodstuffs, restricted goods and goods subject to excise duties in Norway\", \"Examples: Restricted goods\" p.18",
        SKE_VOEC_GUIDELINES_URL,
    ),
    "Skatteetaten VOEC guidelines appendix, restricted goods: \"Foodstuffs, plants, seeds, animals\" / \"The list is not comprehensive or complete. Read more at https://www.toll.no/en/goods/goods-with-import-restrictions/\"",
)
SKE_VOEC_VAT_AREA = Source(
    "W",
    _ref("§2.1 \"Overview – the Norwegian VAT system\" p.4", SKE_VOEC_GUIDELINES_URL),
    "Skatteetaten VOEC guidelines §2.1: \"Please note that the VAT legislation applies to the Norwegian mainland and all areas within the territorial border, but does not include Svalbard, Jan Mayen or the Norwegian dependencies. Sales to these areas are not subject to Norwegian VAT.\"",
)
MVAL_VAT_AREA = Source(
    "W",
    _ref("§ 1-2 (2)", MVAL_URL),
    "Merverdiavgiftsloven § 1-2 (2): \"Med merverdiavgiftsområdet menes det norske fastlandet og alt område innenfor territorialgrensen, men ikke Svalbard, Jan Mayen eller de norske bilandene.\"",
)
BRING_SVALBARD_JAN_MAYEN_POSTAL_CODES = Source(
    "W",
    _ref("rows 8099 and 9170-9178 (postal code, place, municipality code, municipality, category)", BRING_POSTAL_CODE_REGISTER_URL),
    "Posten Norge postal code register: \"8099 JAN MAYEN 2211 JAN MAYEN G\" / \"9170 LONGYEARBYEN 2100 SVALBARD G\" / \"9171 LONGYEARBYEN 2100 SVALBARD P\" / \"9173 NY-ÅLESUND 2100 SVALBARD B\" / \"9174 HOPEN 2100 SVALBARD G\" / \"9175 SVEAGRUVA 2100 SVALBARD G\" / \"9176 BJØRNØYA 2100 SVALBARD G\" / \"9178 BARENTSBURG 2100 SVALBARD G\"; no other code in 9170-9179 is assigned.",
)
HS_VOEC_EXCLUDED_CLASSES = Source(
    "I",
    _ref("chapter and heading beskrivelse fields", TOLLTARIFF_STRUCTURE_URL),
    "No source maps HS codes to the VOEC exclusions; over Tolltariffen's chapter and heading texts the plugin reads chapters 02-04, 07-13, and 15-21 except headings 1209, 1518, 1520, 1521, and 1522, and headings 2201, 2202, 2209, and 2936 as foodstuffs, headings 2203-2208 as alcohol, chapter 24 as tobacco, chapter 30 as pharmaceuticals, chapter 93 as arms and ammunition, and chapters 01 and 06 and heading 1209 as restricted, and leaves chapters 05, 14, and 23 and headings 1518, 1520, 1521, and 1522 unclassified.",
)

ALL: typing.Tuple[Source, ...] = tuple(
    value for value in dict(globals()).values() if isinstance(value, Source)
)
