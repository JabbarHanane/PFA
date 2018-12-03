# -*- coding: utf-8 -*-

from odoo import models, fields


class DelivaryReport(models.Model):
    _name = 'rapport.livraison'

    numero = fields.Many2one('obj.contract', 'numero')
    nom_conducteur = fields.Many2one('obj.client', 'client')
    cin = fields.Char(related='nom_conducteur.cin', string="CIN", store=True, readonly=True)
    vehicule = fields.Many2one('obj.voiture', 'vehicule')
    matricule = fields.Char(related='vehicule.vin_sn', string="Matricule", store=True, readonly=True)
    date_livre = fields.Date('date livre')
    lieu_livraison = fields.Char('lieu de livraison')
    etat = fields.Many2one('obj.ville', 'Etat')
    vignette = fields.Boolean('Vignette')
    carnet = fields.Boolean('Carnet D Entretien')
    autorisation = fields.Boolean('Autorisation de')
    circulation = fields.Boolean('Circulation')
    visite = fields.Boolean('Visite Technique')
    carte = fields.Boolean('Carte Grise')
    att_assurance = fields.Boolean('Att_assurance')
    enjoliveurs = fields.Selection([('1', 'First'), ('2', 'Secound')], string='NB enjoliveurs')
    roue_secours = fields.Selection([('1', 'First'), ('2', 'Secound')], string='Roue de Secours')
    antenne = fields.Selection([('1', 'First'), ('2', 'Secound')], string='Antenne')
    ciqare = fields.Selection([('1', 'First'), ('2', 'Secound')], string='Allurne Ciqare')
    goblet = fields.Selection([('1', 'First'), ('2', 'Secound')], string='Goblet')
    propret = fields.Selection([('1', 'First'), ('2', 'Secound')], string='Propret')
    image1 = fields.Binary('Image1')
    image2 = fields.Binary('Image2')
    notes = fields.Text('Remarques')
