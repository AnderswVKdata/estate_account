from odoo import models, tools
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def set_property_sold(self):
        res = super().set_property_sold()
        tools.logging.warning("estate_account: property sold logic triggered") 
        for property in self:
            partner = property.salesperson_id.partner_id.id
            selling_price = property.selling_price
            self.env['account.move'].create({
                'partner_id': partner,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    (0, 0, {
                        'name': '6% Commission Fee',
                        'quantity': 1.0,
                        'price_unit': selling_price * 0.06,
                    }),
                    (0, 0, {
                        'name': 'Administrative Fees',
                        'quantity': 1.0,
                        'price_unit': 100.0,
                    }),
                ]
            })
        return res
