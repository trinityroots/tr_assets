# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

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
            'all_type': http.request.env['trinityroots.assets.type'].search([]),
            'all_assets': assets_paged,
            'pager': pager
        })

    @http.route('/assets/<model("trinityroots.assets"):assets>/', auth='public', website=True)
    def read_news(self, assets):
        return http.request.render('tr_assets.view_assets', {
            'assets': assets
        })

    @http.route('/assets/search/', auth='public', website=True)
    def search_news(self, keyword, asset_type='all', **kw):
        _logger.warning("Search keyword : " + keyword)
        _logger.warning("Search type : " + asset_type)
        assets = http.request.env['trinityroots.assets']
        if asset_type == 'All' or asset_type == 'all':
            assets_search = assets.search([('asset_address','ilike',keyword)])
        else:
            assets_search = assets.search([('asset_address','ilike',keyword), ('asset_type.id','=',asset_type)])
        return http.request.render('tr_assets.search_result', {
            'keyword': keyword,
            'selected_type': int(asset_type) if asset_type != 'all' else asset_type,
            'all_type': http.request.env['trinityroots.assets.type'].search([]),
            'all_results': assets_search
        })