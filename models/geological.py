from odoo import api, fields, models


class Province(models.Model):
    _name = 'trinityroots.assets.province'
    _description = 'Thailand province model'

    @api.depends('amphoe_ids')
    def _count_total_amphoe(self):
        for rec in self:
            count = 0
            for line in self.amphoe_ids:
                count += 1
            self.total_amphoe = count

    name = fields.Char(string='Name')
    total_amphoe = fields.Integer(string='Total Amphoe', compute='_count_total_amphoe')
    amphoe_ids = fields.One2many(comodel_name='trinityroots.assets.amphoe', inverse_name='province', string='Amphoe List')
    

class Amphoe(models.Model):
    _name = 'trinityroots.assets.amphoe'
    _description = 'Thailand amphoe model'

    name = fields.Char(string='Name')
    province = fields.Many2one(comodel_name='trinityroots.assets.province', string='Province')
    zip_code = fields.Char(string="Zip code")
    