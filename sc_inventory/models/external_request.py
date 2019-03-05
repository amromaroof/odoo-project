# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from odoo import exceptions 


class sc_stock_External(models.Model):
    _name = 'sc.stock.request.external'
    _inherit = ['mail.thread']

    date = fields.Date(readonly=True, default=datetime.now(),)
    unit_id = fields.Many2one('project.unit')

   
    request_line_ids = fields.One2many('sc.stock.request.line.external', 'request_id',required=True)
    user_id = fields.Many2one(
        comodel_name='res.users', string='Made By', default=lambda self: self.env.user)
    department_id = fields.Many2one(
      comodel_name='hr.department', string='Department')
    location_from_id = fields.Many2one(
        comodel_name='stock.location', string='From')
    location_to_id = fields.Many2one(
        comodel_name='stock.location', string='To')
    picking_id = fields.Many2one(comodel_name='stock.picking', string='Picking Refrence')

    picking_type_code = fields.Selection(
        string="Picking Type",
        selection=[
            ('internal', 'Internal'),
            ('outgoing', 'Outgoing'),
            ('incoming', 'Incoming'),
        ], default="outgoing"
    )
    
    state = fields.Selection(
        [('draft', 'Draft'), ('request', 'Manager Director'),
         ('confirm', 'Store Manager'),
         ('done', 'Done')],
        default='draft')


    @api.one
    def request(self):
        self.write({'state': 'request'})

    @api.one
    def confirm(self):
        
        self.write({'state': 'confirm'})

    @api.one
    def second_confirm(self):
        
            self.write({'state': 'second_confirm'})
         
    @api.one
    def done(self):
        self.write({'state': 'done'})
    @api.one
    def check(self):
        self.write({'state': 'check'})




class sc_stock_line_external(models.Model):
    _name = 'sc.stock.request.line.external'

    product_id = fields.Many2one(
        comodel_name='product.product', string='Product' , required=True)
    
    requested_qty = fields.Float(string="Requested Quantity", default=1.0 , required=True)
    approved_qty = fields.Float(string="Aproved Quantity", default=1.0)
    
    
    
    onhand_qty = fields.Float(related="product_id.qty_available",string="Onhand Quantity",store=True)

    product_uom_id = fields.Many2one(comodel_name='product.uom',
                             related="product_id.uom_id", string='Unit of Measure' , required=True)
    request_id = fields.Many2one('sc.stock.request')

#@api.depends('value')
 #def _value_pc(self):
        #self.value2 = float(self.value) / 100




class SC_Stock_picking(models.Model):

    _inherit = 'stock.picking'

    
    department_id = fields.Many2one(
      comodel_name='hr.department', string='Department')
    unit_id = fields.Many2one('project.unit', string='Unit')
    select = fields.Selection(
        [('department', 'Department'), ('unit', 'Unit')], string="Select", default='department')
    requested_qty = fields.Float(string="Requested Quantity", default=1.0 , required=True)


class SC_Stock_picking(models.Model):

    _inherit = 'stock.move'


    requested_qty = fields.Float(string="Requested Quantity", default=1.0 , required=True)