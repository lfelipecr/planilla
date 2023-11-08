# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime


class boleta(models.Model):
    _name = "boleta"
    _inherit = ['mail.thread']
    _description = "Boleta"

    @api.onchange("producto", "peso_kg", "ruta2")
    def change_ruta(self):
        self.precio = self.ruta2.costo_ruta
        self.peso_qq = self.peso_kg / 46

        self.precio_qq = 0
        if len(self.producto):
            for line in self.ruta2.productos:
                if line.name.id == self.producto.id:
                    self.precio_qq = line.costo

        self.total = self.precio_qq * self.peso_qq

    @api.model
    def create(self, vals):
        rec = super(boleta, self).create(vals)
        rec.name = rec.id

        product_id = self.env['product.product'].search([('product_tmpl_id', '=', rec.producto.id)], limit=1)

        registro = self.env['account.analytic.line'].create({
            'name': "Boleta " + str(rec.num_boleta),
            'account_id': rec.cuenta_analitica.id,
            'partner_id': rec.cliente.id,
            'date': rec.date,
            'amount': rec.total,
            'unit_amount': 1,
            'product_id': product_id.id,
            'product_uom_id': product_id.uom_id.id,
        })

        return rec

    name = fields.Char("Consecutivo", tracking=True)
    date = fields.Date("Fecha Entrada", default=datetime.today(), tracking=True)
    placa = fields.Many2one("fleet.vehicle", string="Placa", tracking=True)
    cuenta_analitica = fields.Many2one("account.analytic.account", string="Cuenta A.", tracking=True)
    chofer = fields.Many2one("hr.employee", string="Chofer", tracking=True)
    num_boleta = fields.Char("Num. Boleta", tracking=True)
    cliente = fields.Many2one("res.partner", string="Cliente", tracking=True)
    producto = fields.Many2one("product.template", string="Producto", tracking=True)
    #peso
    peso_kg = fields.Float("Peso Kg.", tracking=True)
    peso_qq = fields.Float("Peso qq.", tracking=True)
    #otros
    tipo = fields.Selection([('produccion', 'Producción'), ('importacion', 'Importación'), ('despacho', 'Despacho'), ('otros', 'Otros')], string="Tipo", tracking=True)
    recargo = fields.Float("Recargo %", tracking=True)
    deduccion = fields.Float("Deducción", tracking=True)
    #ruta
    ruta = fields.Many2one("transportes.rutas", string="Ruta", tracking=True)
    ruta2 = fields.Many2one("boleta_ruta", string="Ruta", tracking=True)
    #origen_destino = fields.Char("Origen/Destino")
    precio = fields.Float("Precio", tracking=True)
    #totals
    precio_qq = fields.Float("Precio x qq.", tracking=True)
    total = fields.Float("Total", tracking=True)


class boleta_ruta_producto(models.Model):
    _name = "boleta_ruta_producto"
    _description = "boleta_ruta_producto"

    name = fields.Many2one("product.template", string="Producto")
    costo = fields.Float("Costo viaje")
    ruta = fields.Many2one("boleta_ruta")


class boleta_ruta(models.Model):
    _name = "boleta_ruta"
    _description = "boleta_ruta"

    @api.onchange("tipo_ruta")
    def change_tipo_ruta(self):
        rutas = self.env['rutas'].search([], limit=1)
        if self.tipo_ruta == "corta":
            self.costo_ruta = rutas.corto
        if self.tipo_ruta == "larga":
            self.costo_ruta = rutas.largo
        if self.tipo_ruta == "bcorta":
            self.costo_ruta = rutas.barco_corto
        if self.tipo_ruta == "blargo":
            self.costo_ruta = rutas.barco_largo
        if self.tipo_ruta == "otras":
            self.costo_ruta = rutas.otras_rutas
        if self.tipo_ruta == False:
            self.costo_ruta = 0

    name = fields.Char("Ruta")
    codigo = fields.Char("Código")
    tipo_ruta = fields.Selection([('corta', 'Ruta Corta'), ('larga', 'Ruta Larga'), ('bcorta', 'Barco Corto'), ('blargo', 'Barco Largo'), ('otras', 'Otras rutas')], string="Tipo Ruta")
    costo_ruta = fields.Float("Precio")
    productos = fields.One2many("boleta_ruta_producto", "ruta")