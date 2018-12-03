# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Pays(models.Model):
    _name = "obj.pays"
    _description = "Objet pays"

    name = fields.Char("Nom ", required=True)
    continent = fields.Selection([('a', 'Afrique'), ('au', 'Austoralie')], "continent", size=64)
