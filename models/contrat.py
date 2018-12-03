# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools, exceptions,_
import datetime
from dateutil.relativedelta import relativedelta


def str_to_datetime(strdate):
    return datetime.datetime.strptime(strdate, tools.DEFAULT_SERVER_DATE_FORMAT)


class fleet_vehicle_log_contract(models.Model):
    _name = 'obj.contract'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'Contract information on a vehicle'
    _order = 'expiration_date'

    @api.multi
    def open_wizard(self):

        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'facture.client',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {'current_id': self.id}
        }

    @api.model
    def create(self, vals):
        res = super(fleet_vehicle_log_contract, self).create(vals)
        voiture = self.env['obj.voiture'].browse(vals['voiture_id'])
        voiture.disponibilite = 'n'
        return res

    @api.one
    @api.depends('expiration_date', 'start_date')
    def get_days(self):
        fin = str_to_datetime(self.expiration_date)
        debut = str_to_datetime(self.start_date)
        self.jours = (fin - debut).days

    @api.one
    @api.depends('voiture_id', 'expiration_date', 'start_date', 'voiture_car_value')
    def get_cout(self):
        self.sum_cost = self.jours * self.voiture_car_value

    @api.constrains('start_date', 'expiration_date')
    def _check_days(self):
        if self.expiration_date <= self.start_date:
            raise exceptions.ValidationError("date fin doit etre plus grande que date debut")

    STATE = [
        ('En cours', 'En cours'),
        ('Termine', 'Termine'),
    ]
    name = fields.Char('Reference du Contrat ', size=64, required=True)

    
    start_date = fields.Date('Date debut de contrat', help='Date a laquelle la couverture du contrat commence',
                             required=True, default=datetime.datetime.today())
    expiration_date = fields.Date('Date fin de contrat', required=True, default=datetime.datetime.today())
    date = fields.Date('Date de la facture', default=datetime.datetime.today())
    sum_cost = fields.Float('le total de la facture', compute='get_cout')
    
    notes = fields.Text('Conditions & termes',
                        help='Write here all supplementary informations relative to this contract')
    client = fields.Many2one("obj.client", 'Client', required=True)
    voiture_id = fields.Many2one("obj.voiture", 'Voiture', required=True)
    odometer = fields.Char('Kilometrage', size=64)
    jours = fields.Integer('le nombre des jours', compute='get_days')
    state = fields.Selection(STATE, string='State', default=lambda *a: 'En cours')
    status_update = fields.Boolean("Status update")

    listprice = fields.Many2one('product.pricelist.item', string='Liste des Prix',
                                domain="[('vehicle_id','=',voiture_id)]")

    facture_id = fields.Many2one('facture.client', 'Facture', readonly=True)
    facturee = fields.Boolean('Contrat Facture', default=False)
    current_user = fields.Many2one('res.users', 'Current User', default=lambda self: self.env.user)

    @api.multi
    def marque_termine(self):
        body = _("Contrat deplace vers termine")
        self.message_post(body=body)
        return self.write({'state': 'Termine', 'status_update': True})

    @api.multi
    def marque_en_cours(self):
        body = _("Contrat deplace vers en cours")
        self.message_post(body=body)
        return self.write({'state': 'En cours', 'status_update': True})

    @api.multi
    def act_renew_contract(self):
        assert len(
            self.ids) == 1, "This operation should only be done for 1 single contract at a time, as it it suppose to open a window as result"
        for element in self:
            # compute end date
            startdate = fields.Date.from_string(element.start_date)
            enddate = fields.Date.from_string(element.expiration_date)
            diffdate = (enddate - startdate)
            default = {
                'date': fields.Date.context_today(self),
                'start_date': fields.Date.to_string(
                    fields.Date.from_string(element.expiration_date) + relativedelta(days=1)),
                'expiration_date': fields.Date.to_string(enddate + diffdate),
            }
            newid = element.copy(default).id
        return {
            'name': _("Renew Contract"),
            'view_mode': 'form',
            'view_id': self.env.ref('notime.fleet_vehicle_log_contract_form').id,
            'view_type': 'tree,form',
            'res_model': 'obj.contract',
            'type': 'ir.actions.act_window',
            'domain': '[]',
            'res_id': newid,
            'context': {'active_id': newid},
        }

    client_reduction = fields.Float(related='client.reduction')
    voiture_car_value = fields.Float(related='listprice.fixed_price')

    @api.multi
    def make_order(self):
        res = []

        modelObj = self.env['product.template']
        client_id = self.env['res.partner'].create({'name': self.client.name})

        for record in self:
            rec = modelObj.search([('name', '=', record.voiture_id.name)])
            if rec:
                order_id = self.env['sale.order'].create(
                    {'or_ti': self.id, 'partner_id': client_id.id, 'order_line': [(0, 0, {'product_id': rec.id, })]})
                self.env['purchase.order'].create({'pur_ti': self.id, 'partner_id': client_id.id, 'order_line': [(0, 0,
                                                                                                                  {
                                                                                                                      'name': 'test',
                                                                                                                      'product_id': rec.id,
                                                                                                                      'product_uom': 1,
                                                                                                                      'price_unit': 1300,
                                                                                                                      'product_qty': 2,
                                                                                                                      'date_planned': datetime.datetime.now()})]})
            else:
                modelObj2 = self.env['product.template'].create({'name': record.voiture_id.name})
                # order_id2 = self.env['sale.order'].create({'or_ti':self.id,'partner_id': self.client.id})
                order_id = self.env['sale.order'].create({'or_ti': self.id, 'partner_id': client_id.id,
                                                          'order_line': [(0, 0, {'product_id': modelObj2.id, })]})
                order_id = self.env['purchase.order'].create({'pur_ti': self.id, 'partner_id': client_id.id,
                                                              'order_line': [(0, 0, {'name': 'test',
                                                                                     'product_id': modelObj2.id,
                                                                                     'product_uom': 1,
                                                                                     'price_unit': 1300,
                                                                                     'product_qty': 2,
                                                                                     'date_planned': datetime.datetime.now()})]})

        return res

    @api.multi
    def Contrat_Imprimer(self):
        self.filtered(lambda s: s.state == 'draft').write({'state': 'sent'})
        return self.env['report'].get_action(self, 'sale.report_saleorder')


class VoiturePrice(models.Model):
    _name = 'obj.voiture.price'
    _inherit = ['mail.thread']

    voiture_id = fields.Many2one('obj.voiture', 'Voiture')
    prix = fields.Float('Prix')
    liste_price_id = fields.Many2one('obj.liste.price')


class ListePrice(models.Model):
    _name = 'obj.liste.price'
    _inherit = ['mail.thread']

    name = fields.Char('Liste des prix')
    voiture_price_ids = fields.One2many('obj.voiture.price', 'liste_price_id', '')


class VoitureLines(models.Model):
    _name = 'voiture.lines'

    @api.depends('voiture')
    def get_prix_voiture(self):
        self.prix = self.voiture.car_value
        return True

    voiture = fields.Many2one('obj.voiture', 'Voiture')
    prix = fields.Float('Cout', compute='get_prix_voiture')
    facture_id = fields.Many2one('facture.client', 'facture')


class FactureClient(models.Model):
    _name = 'facture.client'

    @api.depends('voiture')
    def get_prix_total(self):
        total = 0.0
        active_id = self._context.get('active_ids', [])
        contrat_id = self.env[('obj.contract')].browse(active_id)
        """
        for record in self.voiture:
            total += record.voiture.car_value  #le prix te3 voiture champ esmo prix  
        self.prix_total = total * contrat_id.jours
        self.prix_total_remise = self.prix_total - contrat_id.client_reduction
        return self.prix_total
        """
        self.prix_total = self.contrat_id.sum_cost
        return self.prix_total

    @api.one
    def get_contrat(self):
        active_id = self._context.get('active_ids', [])
        self.contrat_id = self.env[('obj.contract')].browse(active_id)
        return self.contrat_id

    @api.depends('contrat_id')
    def get_defaut_value_client(self):
        self.client = self.contrat_id.client.id
        return self.client

    @api.depends('contrat_id')
    def get_defaut_value_voiture(self):
        self.voiture = self.contrat_id.voiture_id.id
        return self.voiture

    STATE = [
        ('En cours', 'En cours'),
        ('Termine', 'Termine'),
    ]

    @api.one
    def paye_abonnement(self):
        self.payee = True
        self.state = 'Termine'
        self.contrat_id.facture_id = self.id
        self.contrat_id.facturee = True
        return True

    name = fields.Char('Reference Facture')
    client = fields.Many2one('obj.client', 'Client', compute='get_defaut_value_client', store=True)
    voiture = fields.Many2one('obj.voiture', 'Voiture', compute='get_defaut_value_voiture',
                              store=True)  # client ??? objet
    prix_total = fields.Float('Somme', compute='get_prix_total', store=True)
    payee = fields.Boolean('facture payee', store=True, default=False)
    contrat_id = fields.Many2one('obj.contract', 'Contrat', default=get_contrat, store=True)
    state = fields.Selection(STATE, string='State', default=lambda *a: 'En cours')
    prix_total_remise = fields.Float('Prix total', compute='get_prix_total', store=True)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    or_ti = fields.Many2one('obj.contract')


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    pur_ti = fields.Many2one('obj.contract')
    client = fields.Many2one('res.partner', string="client")
    vehicle_id = fields.Many2one('obj.voiture')
