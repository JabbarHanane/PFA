# -*- coding: utf-8 -*-
from odoo import models, fields


class Modele(models.Model):
    _name = "obj.modele"
    _description = "Objet modele"

    name = fields.Char("Nom de modèle(marque/modéle)  ", required=True)
