# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class Assets(models.Model):
    _name="trinityroots.assets"
    _description="This module is for managing assets"
    _rec_name="asset_code"

    @api.onchange('asset_deed_ids')
    def _count_total_deeds(self):
        for rec in self:
            rec.asset_total_deed = rec.asset_deed_ids.search_count([('assets_owner','=',self.id)])

    #fields
    asset_code = fields.Char(
        string="Asset Code",
        required=True
    )

    asset_type = fields.Many2one(
        comodel_name='trinityroots.assets.type',
        string='Asset Type'
    )

    asset_deed_ids = fields.One2many(
        comodel_name='trinityroots.assets.deed',
        inverse_name='assets_owner',
        string='Asset Deeds'
    )

    #TODO compute field from asset_deed
    asset_total_deed = fields.Integer(
        string='Total Asset Deeds',
        compute='_count_total_deeds'
    )

    asset_area = fields.Char(
        string='Asset Area'
    )

    asset_address = fields.Char(
        string='Asset Address'
    )

    asset_color = fields.Many2one(
        comodel_name='trinityroots.assets.color',
        string='Asset Color'
    )
    
    asset_road_frontage = fields.Char(
        string='Asset Road Frontage'
    )

    asset_price = fields.Float(
        string='Asset Price'
    )

    asset_promo_toggle = fields.Boolean(
        string='Show Promotion'
    )

    asset_promo = fields.Text(
        string='Promotion'
    )

    asset_image_ids = fields.One2many(comodel_name='trinityroots.assets.image', inverse_name='owner', string='Images')

    asset_description = fields.Html(string='Asset Description')

    asset_access = fields.Text(
        string='Asset Access Description'
    )

    asset_latlong = fields.Char(string="GPS Location")
    
class AssetsColor(models.Model):
    _name="trinityroots.assets.color"
    _description="Assets Color"
    
    #fields
    name = fields.Char(
        string='Color'
    )

    description = fields.Text(
        string='Description'
    )
    
    color_code = fields.Char(
        string="Color Hex Code"
    )

    is_publish = fields.Boolean(
        string="Publish",
        default=True
    )

class AssetsType(models.Model):
    _name = 'trinityroots.assets.type'
    _description = 'Assets Type Model'

    name = fields.Char(string='Type')

class AssetsDeeds(models.Model):
    _name = 'trinityroots.assets.deed'
    _description = 'Assets Deed Model'

    name = fields.Char(string='Deeds ID')

    assets_owner = fields.Many2one(comodel_name='trinityroots.assets', string='Assets Owner')
    
class AssetsImage(models.Model):
    _name = "trinityroots.assets.image"
    _inherit = ['ir.attachment']
    _description = 'Assets Image Model'

    #image = fields.Binary()
    #name = fields.Char(string='Image Name')
    #datas = fields.Binary(string='File')
    is_main = fields.Boolean(string='Is Main Picture')
    sequence = fields.Integer(string='Sequence')
    owner = fields.Many2one(comodel_name='trinityroots.assets', string='Owner')