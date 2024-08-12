# Copyright 2022 Stéphan Sainléger (Elabore)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "partner_profiles_portal",
    "version": "17.0.1.0.0",
    "author": "Elabore",
    "website": "https://elabore.coop",
    "maintainer": "Stéphan Sainléger",
    "license": "AGPL-3",
    "category": "Tools",
    "summary": "Provide portal pages and forms to manage partner's profiles from portal home space.",
    # any module necessary for this one to work correctly
    "depends": [
        "base",
        "partner_contact_in_several_companies",
        "partner_profiles",
        "portal",
        "website",
    ],
    "qweb": [],
    "external_dependencies": {
        "python": [],
    },
    # always loaded
    "data": [
        "security/members_security.xml",
        "views/portal_home_template.xml",
        "views/portal_my_structures_template.xml",
        "views/portal_my_positions_template.xml",
        "views/portal_partner_structure_template.xml",
        "views/portal_partner_position_template.xml",
        "views/portal_my_account.xml",
        "views/res_partner_view.xml",
        "wizard/create_position_profile.xml",
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
