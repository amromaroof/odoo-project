
from odoo import models, fields, api
from datetime import datetime
from odoo import exceptions 

class sc_stock(models.Model):
    _name = 'sc.stock.request'
    _inherit = ['mail.thread']

    date = fields.Date(readonly=True, default=datetime.now(),)
    unit_id = fields.Many2one('project.unit')

    select = fields.Selection(
        [('department', 'Department'), ('unit', 'Unit')])
    request_line_ids = fields.One2many('sc.stock.request.line', 'request_id',required=True)
    user_id = fields.Many2one(
        comodel_name='res.users', string='Made By', default=lambda self: self.env.user)
    department_id = fields.Many2one(
      comodel_name='hr.department', string='Department')
    # location_id = fields.Many2one(
    #     comodel_name='stock.location', string='From')
    # location_dest_id = fields.Many2one(
    #     comodel_name='stock.location', string='To')
    
    state = fields.Selection(
        [('draft', 'Draft'), ('request', 'Request'),
         ('confirm', 'Manager Director'),('second_confirm', 'Store Manager'),
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

        rec=self.env['stock.picking'].create(
            {
              # 'location_id': self.location_id
              # 'location_dest_id': self.location_dest_id
               # 'origin':self.date
            })
        for line in self.request_line_ids:
            rec.write({'move_lines':[(0,0,{'s':line.product_id.id,'product_qty':line.approved_qty})]})
            
        
        self.write({'state': 'second_confirm'})
         
    @api.one
    def done(self):
        self.write({'state': 'done'})
    @api.one
    def check(self):
        self.write({'state': 'check'})




class sc_stock_line(models.Model):
    _name = 'sc.stock.request.line'

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

class res_users(models.Model):

    _inherit = 'stock.picking'

    picking_type_id=fields.Many2one('stock.picking.type')
    location_id = fields.Many2one(
        'stock.location', "Source Location",
        default=lambda self: self.env['stock.picking.type'].browse(self._context.get('default_picking_type_id')).default_location_src_id)
