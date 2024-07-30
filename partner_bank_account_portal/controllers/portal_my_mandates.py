# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http, _
from odoo.osv import expression
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.exceptions import AccessError, MissingError
from collections import OrderedDict
from odoo.http import request


class CustomerPortalMandates(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'mandate_count' in counters:
            mandate_count = request.env['account.banking.mandate'].search_count([])
            values['mandate_count'] = mandate_count
        return values

    @http.route(['/my/mandates', '/my/mandates/page/<int:page>'], type='http', auth="user", website=True)
    def portal_mandates(self, page=1, date_begin=None, date_end=None, filterby=None, **kw):
        values = self._prepare_my_mandates_values(page, date_begin, date_end)

        # pager
        pager = portal_pager(**values['pager'])

        # content according to pager and archive selected
        mandates = values['mandates'](pager['offset'])
        request.session['mandates_history'] = mandates.ids[:100]

        values.update({
            'mandates': mandates,
            'pager': pager,
        })
        return request.render("partner_bank_account_portal.portal_my_mandates", values)

    def _get_mandate_domain(self):
        return []

    def _prepare_my_mandates_values(self, page, date_begin, date_end, domain=None, url="/my/mandates"):
        values = self._prepare_portal_layout_values()
        Mandate = request.env['account.banking.mandate']

        domain = expression.AND([
            domain or [],
            self._get_mandate_domain(),
        ])
        
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        values.update({
            'date': date_begin,
            # content according to pager and archive selected
            # lambda function to get the invoices recordset when the pager will be defined in the main method of a route
            'mandates': lambda pager_offset: (
                Mandate.search(domain, limit=self._items_per_page, offset=pager_offset)
                if Mandate.check_access_rights('read', raise_exception=False) else
                Mandate
            ),
            'page_name': 'mandates',
            'pager': {  # vals to define the pager.
                "url": url,
                "url_args": {'date_begin': date_begin, 'date_end': date_end},
                "total": Mandate.search_count(domain) if Mandate.check_access_rights('read', raise_exception=False) else 0,
                "page": page,
                "step": self._items_per_page,
            },
            'default_url': url,
        })
        return values
