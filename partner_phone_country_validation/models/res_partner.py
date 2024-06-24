from odoo import api, models, _
from odoo.addons.partner_phone_country_validation.tools.get_country_from_phone_number import get_country_from_phone_number
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class Partner(models.Model):
    _name = 'res.partner'
    _inherit = ['res.partner', 'phone.validation.mixin']

    @api.constrains('country_id','phone','mobile')
    def _check_country_id(self):
        
        #if come back quote creation from lead, update partner
        country = False
        if self._context.get("default_type") == 'opportunity' and self._context.get("params").get("model") == "crm.lead":
            lead = self.env["crm.lead"].browse(self._context.get("params").get("id"))
            country = lead.country_id
            for partner in self:
                if not country and (partner.phone or partner.mobile):
                    if self.phone:
                        partner.set_country_from_phone_number(partner.phone)
                    if self.mobile:
                        partner.set_country_from_phone_number(partner.mobile)
                elif country:
                    partner.country_id = country
                            
        #check country and raise error
        for partner in self:
            if not partner.country_id and not partner.parent_id.country_id and (partner.phone or partner.mobile):
                raise ValidationError(_('You must set a country for the phone number of %s'%(partner.name,)))
        
    @api.onchange('country_id')
    def _onchange_country(self):
        self.format_mobile_from_country()
        self.format_phone_from_country()

    def format_number_zerozero(self, number):
        if number.startswith("00"):
            number = "+"+number[2:]
        return number

    def format_phone_from_country(self):
        if self.phone:            
            country = None
            if self.phone.startswith('+'):
                country = self.env['res.country'].search(
                    [('code', '=', get_country_from_phone_number(self.phone))], limit=1
                )
            if self.country_id:
                country = self.country_id
            if country:
                self.phone = self.phone_format(self.phone, country=country)

    def format_mobile_from_country(self):
        if self.mobile:            
            country = None
            if self.mobile.startswith('+'):
                country = self.env['res.country'].search(
                    [('code', '=', get_country_from_phone_number(self.mobile))], limit=1
                )
            if self.country_id:
                country = self.country_id
            if country:
                self.mobile = self.phone_format(self.mobile, country=country)

    def set_country_from_phone_number(self, phone_number):
        country = self.env['res.country'].search(
            [('code', '=', get_country_from_phone_number(phone_number))], limit=1
        )
        if country and not self.country_id:
            self.country_id = country

    @api.onchange('phone')
    def _onchange_phone_validation(self):
        # If no country is found, we define the country based on the beginning of the number
        if self.phone:
            self.phone = self.format_number_zerozero(self.phone)
            self.set_country_from_phone_number(self.phone)
            self.format_phone_from_country()
        

    @api.onchange('mobile')
    def _onchange_mobile_validation(self):
        # If no country is found, we define the country based on the beginning of the number
        if self.mobile:
            self.mobile = self.format_number_zerozero(self.mobile)
            self.set_country_from_phone_number(self.mobile)
            self.format_mobile_from_country()