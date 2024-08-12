{
    "name": "partner_gogocarto_export_api",
    "summary": """HTTP JSON api to send partner data for Gogocarto import""",
    "license": "AGPL-3",
    "author": ("Lokavaluto", "Elabore"),
    "website": "https://lokavaluto.fr",
    "category": "Localization",
    "version": "17.0.1.0.0",
    "depends": [
        "base",
        "contacts",
        "base_geolocalize",
        "jsonifier",
        "partner_geolocalize_usability",
    ],
    "data": [
        "views/gogocarto_partner.xml",
        "views/gogocarto_config_settings_view.xml",
        "views/res_company_view.xml",
    ],
    "demo": [],
    "installable": True,
    "auto_install": False,
}
