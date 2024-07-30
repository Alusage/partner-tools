# Copyright 2020 Lokavaluto ()
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import base64
from odoo import http, tools, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortalBankAccount(CustomerPortal):

    def _bank_account_get_page_view_values(self, bank_account, access_token, **kwargs):
        values = {
            "page_name": "bank_account",
            "bank_account": bank_account,
        }
        return self._get_page_view_values(
            bank_account, access_token, values, "my_bank_accounts_history", False, **kwargs
        )

    def _details_bank_account_form_validate(self, data, bank_account_id):
        error = dict()
        error_message = []
        # public name uniqueness
        if data.get("public_name") and request.env["res.partner"].sudo().search(
            [
                ("name", "=", data.get("public_name")),
                ("is_public_profile", "=", True),
                ("contact_id", "!=", bank_account_id),
            ]
        ):
            error["public_name"] = "error"
            error_message.append(
                _("This public name is already used, please find an other idea.")
            )

        # email validation
        if data.get("email") and not tools.single_email_re.match(data.get("email")):
            error["email"] = "error"
            error_message.append(
                _("Invalid Email! Please enter a valid email address.")
            )
        return error, error_message

    def _get_bank_account_fields(self):
        fields = [
            "acc_number",
            "bank_id",
            "acc_holder_name",
        ]
        return fields

    def _get_main_boolean_bank_account_fields(self):
        '''Provides the fields for which we must check the presence
        in form's kw to know the value to save in the partner field.
        All of them MUST start with "main_".'''
        fields = []
        return fields

    def _transform_in_res_partner_fields(self, kw, bank_account_fields, prefix=""):
        '''Transforms kw's values in res_partner fields and values'''
        return {key[len(prefix):]: kw[key] for key in bank_account_fields if key in kw}

    def _add_boolean_values(self, values, kw, boolean_fields, prefix=""):
        for key in boolean_fields:
            values.update(
                {
                    key[len(prefix):]: kw.get(key, "off") == "on",
                }
            )
        return values

    def _get_page_saving_bank_account_values(self, kw):
        bank_account_fields = self._get_bank_account_fields()
        values = self._transform_in_res_partner_fields(kw, bank_account_fields)
        # boolean_fields = self._get_main_boolean_bank_account_fields()
        # values = self._add_boolean_values(values, kw, boolean_fields)
        return values

    def _get_page_opening_values(self):
        # Just retrieve the values to display for Selection fields
        countries = request.env["res.country"].sudo().search([])
        values = {
            "countries": countries,
        }
        return values

    @http.route(
        ["/my/bank_account/<int:bank_account_id>", "/my/bank_account/save"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_bank_account(
        self,bank_account_id=None, access_token=None, redirect=None, **kw
    ):
        # The following condition is to transform profile_id to an int, as it is sent as a string from the templace "portal_my_profile"
        # TODO: find a better way to retrieve the profile_id at form submit step
        if not isinstance(bank_account_id, int):
            bank_account_id = int(bank_account_id)

        # Check that the user has the right to see this profile
        try:
            bank_account_sudo = self._document_check_access(
                "res.partner.bank", bank_account_id, access_token
            )
        except (AccessError, MissingError):
            return request.redirect("/my/bank_accounts")

        PartnerBankAccount = request.env["res.partner.bank"]
        user = request.env.user
        bank_account = PartnerBankAccount.browse(bank_account_id)

        values = self._bank_account_get_page_view_values(bank_account_sudo, access_token, **kw)
        values.update(
            {
                "error": {},
                "error_message": [],
            }
        )
        if kw and request.httprequest.method == "POST":
            # the user has clicked in the Save button to save new data
            error, error_message = self._details_bank_account_form_validate(kw, bank_account_id)
            values.update({"error": error, "error_message": error_message})
            values.update(kw)
            if not error:
                # Update main profile
                new_values = self._get_page_saving_bank_account_values(kw)
                bank_account.sudo().write(new_values)
                # Update public profile
                # new_values = self._get_page_saving_public_structure_values(kw)
                # public_profile.sudo().write(new_values)
                # Update position profile
                # new_values = self._get_page_saving_position_structure_values(kw)
                # position_profile.sudo().write(new_values)
                # End of updates
                if redirect:
                    return request.redirect(redirect)
                return request.redirect("/my/bank_accounts")

        # This is just the form page opening. We send all the data needed for the form fields
        can_edit_bank_account = user.partner_id == bank_account.partner_id
        values.update(self._get_page_opening_values())
        values.update(
            {
                "bank_account_id": bank_account_id, # Sent in order to retrieve it at submit time
                "can_edit_bank_account": can_edit_bank_account,
                "redirect": "/my/bank_account/" + str(bank_account_id) + "?success=True"
            }
        )
        return request.render("partner_bank_account_portal.portal_my_bank_account", values) #TODO créer le template portal_my_bank_account.xml
