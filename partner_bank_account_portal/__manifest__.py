# Copyright 2022 Stéphan Sainléger (Elabore)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "partner_bank_account_portal",
    "version": "16.0.1.0.0",
    "author": "Elabore",
    "website": "https://elabore.coop",
    "maintainer": "Laetitia Da Costa",
    "license": "AGPL-3",
    "category": "Tools",
    "summary": "Provide portal pages and forms to manage partner's contract, bank accounts and mandates from portal home space.",
    # any module necessary for this one to work correctly
    "depends": [
        "base",
        "account",
        "portal",
        "website",
        "account_banking_mandate",
        "contract",
    ],  
    "qweb": [],
    "external_dependencies": {
        "python": [],
    },
    # always loaded
    "data": [
        "security/members_security.xml",
        "security/ir.model.access.csv",
        "views/portal_my_home_template.xml",
        "views/portal_my_bank_accounts_template.xml",
        "views/portal_my_bank_account_template.xml",
        "views/portal_my_mandates_template.xml",
        "views/portal_my_mandate_template.xml",
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