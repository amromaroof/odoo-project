# -*- coding: utf-8 -*-
from odoo import http

# class ScInventory(http.Controller):
#     @http.route('/sc_inventory/sc_inventory/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sc_inventory/sc_inventory/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sc_inventory.listing', {
#             'root': '/sc_inventory/sc_inventory',
#             'objects': http.request.env['sc_inventory.sc_inventory'].search([]),
#         })

#     @http.route('/sc_inventory/sc_inventory/objects/<model("sc_inventory.sc_inventory"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sc_inventory.object', {
#             'object': obj
#         })