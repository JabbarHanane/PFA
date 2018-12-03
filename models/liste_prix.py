
from odoo import models, fields, api, _


class ListePrix(models.Model):
    _inherit = 'product.pricelist.item'

    client = fields.Many2one('res.partner', string="client")
    vehicle_id = fields.Many2one('obj.voiture')
    prix_fx = fields.Float(string="prix")
    Name = fields.Char("Nom")
    etat = fields.Selection([
        ('ete', 'ete'),
        ('hiver', ' hiver'), ('printemps', ' printemps'), ('automne', ' automne')], "etat",
        required=True)
    applied = fields.Selection([

        ('2_vehicle', ' vehicule')], "Apply On",
        default='2_vehicle', required=True)

    @api.onchange('applied')
    def _onchange_applied_on(self):
        if self.applied != '1_client':
            self.client = False
        if self.applied != '2_vehicle':
            self.vehicle_id = False

    @api.one
    @api.depends('vehicle_id', 'client', 'compute_price', 'fixed_price', \
                 'pricelist_id', 'percent_price', 'price_discount', 'price_surcharge')
    def _get_pricelist_item_name_price(self):
        if self.Name:
            self.name = self.Name
        if self.compute_price == 'fixed':
            self.price = (self.fixed_price, self.pricelist_id.currency_id.name)
        elif self.compute_price == 'percentage':
            self.price = (self.percent_price)
        else:
            self.price = _("%s %% discount and %s surcharge") % (self.price_discount, self.price_surcharge)

    @api.model
    @api.depends('fixed_price')
    def create(self, vals):
        res = super(ListePrix, self).create(vals)
        voiture = self.env['obj.voiture'].browse(vals['vehicle_id'])
        voiture.car_value = vals['fixed_price']
        return res
