# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class Assets(http.Controller):
    @http.route([
        '''/assets''',
        '''/assets/page/<int:page>'''
        ], auth='public', website=True)
    def listing(self, page=0, **kw):
        assets_model = http.request.env['trinityroots.assets']
        all_assets = assets_model.search([])
        assets_count = len(all_assets)
        pager = request.website.pager(url='/assets', total=assets_count, page=page, step=8, scope=7, url_args=kw)

        assets_paged = assets_model.search([], limit=8, offset=pager['offset'])
        return http.request.render('tr_assets.index', {
            'all_assets': assets_paged,
            'pager': pager
        })

    @http.route('/assets/<model("trinityroots.assets"):assets>/', auth='public', website=True)
    def read_news(self, assets):
        return http.request.render('tr_assets.view_assets', {
            'assets': assets
        })