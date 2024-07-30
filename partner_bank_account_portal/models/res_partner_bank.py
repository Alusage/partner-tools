# Copyright 2022 Elabore (https://elabore.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models

class res_partner_bank(models.Model):
    _inherit = "res.partner.bank"

    #count all mandate linked to the IBAN, even draft or canceled mandates
    associated_mandate_count = fields.Integer("Associated mandate count", compute="_compute_associated_mandate_count")

    def _compute_associated_mandate_count(self):
        for record in self:
            count = self.env["account.banking.mandate"].search_count(
                [("partner_bank_id", "=", record.id)]
            )
            record.associated_mandate_count = count