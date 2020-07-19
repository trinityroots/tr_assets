# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class Assets(models.Model):
    _name="trinityroots.assets"
    _description="This module is for managing assets"
    _rec_name="asset_code"


    @api.depends('asset_deed_ids')
    def _count_total_deeds(self):
        for rec in self:
            count = 0
            for line in self.asset_deed_ids:
                count += 1
            self.asset_total_deed = count

    @api.onchange('asset_image_ids')
    def _check_duplicate_sequence(self):
        for rec in self:
            existing = []
            for line in rec.asset_image_ids:
                if line.sequence in existing:
                    raise ValidationError('Sequence should be unique')
                existing.append(line.sequence)
                _logger.warning(line)
            _logger.warning(rec)

    @api.onchange('asset_image_ids')
    def _check_multi_main_img(self):
        for rec in self:
            existing = False
            for line in rec.asset_image_ids:
                if line.is_main is True:
                    if existing is True:
                        raise ValidationError('Main image should have only one')
                    else:
                        existing = True

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

    def checkType(self, x):
        return str(type(x))

    name = fields.Char(string='Type')

class AssetsDeeds(models.Model):
    _name = 'trinityroots.assets.deed'
    _description = 'Assets Deed Model'

    name = fields.Char(string='Deeds ID')

    assets_owner = fields.Many2one(comodel_name='trinityroots.assets', string='Assets Owner')
    
class AssetsImage(models.Model):
    _name = "trinityroots.assets.image"
    _description = 'Assets Image Model'
    _order = "sequence asc"

    #TODO when is_main is true -> sequence force as 0
    #TODO sequence is not duplicate
    #TODO preview image as in form view (use widget and sort sequence?)

    @api.onchange('is_main')
    def _main_image_at_zero(self):
        if self.is_main is True:
            self.sequence = 1

    name = fields.Char(name="Image name")
    datas = fields.Binary(string='Image Data')
    is_main = fields.Boolean(string='Is Main Picture')
    sequence = fields.Integer(string='Sequence')
    owner = fields.Many2one(comodel_name='trinityroots.assets', string='Owner')