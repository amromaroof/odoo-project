# -*- coding: utf-8 -*-

from odoo import models, fields, api

class res_users(models.Model):

    _inherit = 'stock.picking'

    picking_type_id=fields.Many2one('stock.picking.type')
    location_id = fields.Many2one(
        'stock.location', "Source Location",
        default=lambda self: self.env['stock.picking.type'].browse(self._context.get('default_picking_type_id')).default_location_src_id)
        