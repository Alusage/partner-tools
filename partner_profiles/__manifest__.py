# Copyright 2022 Stéphan Sainléger (Elabore)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "partner_profiles",
    "version": "17.0.1.0.0",
    "author": "Elabore",
    "website": "https://elabore.coop",
    "maintainer": "Stéphan Sainléger",
    "license": "AGPL-3",
    "category": "Tools",
    "summary": "Provide several profiles for one person.",
    # any module necessary for this one to work correctly
    "depends": [
        "base",
        "calendar",
        "contacts",
        "partner_contact_in_several_companies",
    ],
    "qweb": [
        # "static/src/xml/*.xml",
    ],
    "external_dependencies": {
        "python": [],
    },
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "wizard/create_position_profile.xml",
        "views/res_partner_view.xml",
        "views/partner_profile_view.xml",
        "data/partner_profile_data.xml",
        "data/res_partner_data.xml",
    ],
    # only loaded in demonstration mode
    "demo": [],
    "js": [],
    "css": [],
    "installable": True,
    # Install this module automatically if all dependency have been previously
    # and independently installed.  Used for synergetic or glue modules.
    "auto_install": False,
    "application": False,
}
