# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http, _
from odoo.osv import expression
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.exceptions import AccessError, MissingError
from collections import OrderedDict
from odoo.http import request


class CustomerPortalBankAccounts(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'bank_account_count' in counters:
            bank_account_count = request.env['res.partner.bank'].search_count([])
            values['bank_account_count'] = bank_account_count
        return values

    def _get_account_searchbar_sortings(self):
        res = super()._get_account_searchbar_sortings()
        res['acc_number'] = {'label': _('IBAN'), 'order': 'acc_number'}
        return res



    @http.route(['/my/bank_accounts', '/my/bank_accounts/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_bank_accounts(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
        values = self._prepare_my_bank_accounts_values(page, date_begin, date_end, sortby, filterby)

        # pager
        pager = portal_pager(**values['pager'])

        # content according to pager and archive selected
        bank_accounts = values['bank_accounts'](pager['offset'])
        request.session['bank_accounts_history'] = bank_accounts.ids[:100]

        values.update({
            'bank_accounts': bank_accounts,
            'pager': pager,
        })
        return request.render("partner_bank_account_portal.portal_my_bank_accounts", values)

    def _get_bank_accounts_domain(self):
        return [('active', '=', True)]


    def _prepare_my_bank_accounts_values(self, page, date_begin, date_end, sortby, filterby, domain=None, url="/my/bank_accounts"):
        values = self._prepare_portal_layout_values()
        res_partner_bank = request.env['res.partner.bank']

        domain = expression.AND([
            domain or [],
            self._get_bank_accounts_domain(),
        ])

        searchbar_sortings = self._get_account_searchbar_sortings()
        # default sort by order
        if not sortby:
            sortby = 'acc_number'
        order = searchbar_sortings[sortby]['order']

        # default filter by value
        if not filterby:
            filterby = 'all'

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        values.update({
            'date': date_begin,
            # content according to pager and archive selected
            # lambda function to get the invoices recordset when the pager will be defined in the main method of a route
            'bank_accounts': lambda pager_offset: (
                res_partner_bank.search(domain, order=order, limit=self._items_per_page, offset=pager_offset)
                if res_partner_bank.check_access_rights('read', raise_exception=False) else
                res_partner_bank
            ),
            'page_name': 'bank_accounts',
            'pager': {  # vals to define the pager.
                "url": url,
                "url_args": {'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
                "total": res_partner_bank.search_count(domain) if res_partner_bank.check_access_rights('read', raise_exception=False) else 0,
                "page": page,
                "step": self._items_per_page,
            },
            'default_url': url,
            'sortby': sortby,
            'filterby': filterby,
        })
        return values
