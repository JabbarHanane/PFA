# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Voiture(models.Model):
    _name = "obj.voiture"
    _description = "Objet voiture"

    name = fields.Char('Modèle', required=True)
    license_plate = fields.Char('Plaque d immatriculation', size=32, required=True)
    vin_sn = fields.Char('Numéro de chassis', size=32, required=True)
    acquisition_date = fields.Date('Date d acquisition', required=False)
    color = fields.Char('Couleur', size=32, help='Color of the vehicle')
    image_medium = fields.Binary("Image")
    carte_grise = fields.Binary("carte grise")

    location = fields.Char('Lieu', size=128)
    seats = fields.Integer('Nombre de places', required=True)
    doors = fields.Integer('Nombre de portes', default=5)
    odometer = fields.Char('Dernier relevé kilomètrique', size=128)
    odometer_unit = fields.Selection([('kilometers', 'Kilométeres'), ('miles', 'Miles')], 'Odometer Unit',
                                     default='kilometers')
    transmission = fields.Selection([('manual', 'Manualle'), ('automatic', 'Automatique')], 'Transmission')
    fuel_type = fields.Selection(
        [('gasoline', 'Essense'), ('diesel', 'Diesel'), ('electric', 'Electrique'), ('hybrid', 'Hybride')],
        'Type de carburant')
    horsepower = fields.Integer('Nombre de chevaux')
    horsepower_tax = fields.Float('Taxe sur la puissance (en chevaux fiscaux)')
    power = fields.Integer('Puissance (kW)')
    co2 = fields.Float('Emissions de CO2')
    car_value = fields.Float('Cout de la voiture', required=True)
    disponibilite = fields.Selection([('d', 'Disponible'), ('n', 'Non disponible')], 'disponibilité', default='d')
    Classe = fields.Selection([('e', 'Economique'), ('l', 'Luxe')], 'Classe')
    count_contracts = fields.Float('Number of Contrats', compute='get_count_smart_buttons')

    @api.one
    def get_count_smart_buttons(self):
        self.count_contracts = self.env['obj.contract'].search_count([('voiture_id', '=', self.id)])

    @api.multi
    def open_contracts(self):
        return {
            'domain': [('voiture_id', '=', self.id)],
            'name': 'Contrats',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'obj.contract',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'context': {}
        }
