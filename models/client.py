# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Client(models.Model):
    _name = "obj.client"
    _description = "Objet client"

    name = fields.Char("Nom complet", required=True)
    num_permis = fields.Char("numéro de permis ", required=True)
    cin = fields.Char("CIN", required=True)
    date_nais = fields.Date("Date de naissance", required=True)
    tel = fields.Char("Tél")
    tel_portable = fields.Char("Tél portable", required=True)
    fax = fields.Char("Fax")
    courriel = fields.Char("Courriel", required=True)
    civilite = fields.Selection([('f', 'Madame'), ('h', 'Monsieur')], "Civilité", size=10, required=True)
    adresse = fields.Char("Adresse", required=True)
    ville = fields.Many2one("obj.ville", "Ville", required=True)
    pays = fields.Many2one("obj.pays", "Pays", required=True)
    code_pos = fields.Char("Code postal")
    count_contracts = fields.Float('Number of Contrats', compute='get_count_smart_buttons')
    reduction = fields.Float("Réduction", default='0.0')

    @api.one
    def get_count_smart_buttons(self):
        self.count_contracts = self.env['obj.contract'].search_count([('client', '=', self.id)])

    @api.multi
    def open_contracts(self):
        return {
            'domain': [('client', '=', self.id)],
            'name': 'Contrats',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'obj.contract',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'context': {}
        }
