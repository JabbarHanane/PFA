# -*- coding: utf-8 -*-

from odoo import models, fields


class Ville(models.Model):
    _name = "obj.ville"
    _description = "Objet ville"

    name = fields.Char("Nom ", required=True)
