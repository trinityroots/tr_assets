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
            'all_province': http.request.env['trinityroots.assets.province'].search([]),
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
    def search_news(self, keyword='', asset_type='all', province='all', amphoe='all', **kw):
        _logger.warning("Search keyword : " + keyword)
        _logger.warning("Search type : " + asset_type)
        _logger.warning("Search Province : " + province)
        _logger.warning("Search Amphoe : " + amphoe)
        assets = http.request.env['trinityroots.assets']

        return_obj = {
            'keyword': keyword,
            'all_type': http.request.env['trinityroots.assets.type'].search([]),
            'all_province': http.request.env['trinityroots.assets.province'].search([]),
            'selected_type': int(asset_type) if asset_type != 'all' else asset_type,
            'selected_province': int(province) if province != 'all' else province,
            'selected_amphoe': int(amphoe) if amphoe != 'all' else amphoe,
        }

        search_domain = []
        if keyword != '':
            search_domain.append(('asset_address','ilike',keyword))
        if asset_type != 'all':
            search_domain.append(('asset_type.id','=',asset_type))
        if province != 'all':
            province = http.request.env['trinityroots.assets.province'].browse([int(province)])
            search_domain.append(('asset_address','ilike',province.name))
            all_amphoe = http.request.env['trinityroots.assets.amphoe'].search([('province.id','=',int(province))])
            return_obj.update({'all_amphoe': all_amphoe})
        if amphoe != 'all':
            #search_domain.pop()
            amphoe = http.request.env['trinityroots.assets.amphoe'].browse([int(amphoe)])
            search_domain.append(('asset_address','ilike',amphoe.name[3:]))
        
        assets_search = assets.search(search_domain)
        return_obj.update({'all_results': assets_search})

        return http.request.render('tr_assets.search_result', return_obj)

    @http.route('/api/', auth='public')
    def index(self, province_id='', **kw):
        html = '<option value="all">All</option>'
        if province_id == 'all' or province_id == '':
            pass
        else:
            amphoe = http.request.env['trinityroots.assets.amphoe'].search([('province.id','=',province_id)])
            #_logger.warning(amphoe)
            for rec in amphoe:
                #_logger.warning(rec.name)
                html += '<option value="'+str(rec.id)+'">'+rec.name+'</option>'
        return html