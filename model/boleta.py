# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime


class boleta(models.Model):
    _name = "boleta"
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
        return rec

    name = fields.Char("Consecutivo")
    date = fields.Date("Fecha Entrada", default=datetime.today())
    placa = fields.Many2one("fleet.vehicle", string="Placa")
    chofer = fields.Many2one("hr.employee", string="Chofer")
    num_boleta = fields.Char("Num. Boleta")
    cliente = fields.Many2one("res.partner", string="Cliente")
    producto = fields.Many2one("product.template", string="Producto")
    #peso
    peso_kg = fields.Float("Peso Kg.")
    peso_qq = fields.Float("Peso qq.")
    #otros
    tipo = fields.Selection([('produccion', 'Producción'), ('importacion', 'Importación'), ('despacho', 'Despacho'), ('otros', 'Otros')], string="Tipo")
    recargo = fields.Float("Recargo %")
    deduccion = fields.Float("Deducción")
    #ruta
    ruta = fields.Many2one("transportes.rutas", string="Ruta")
    ruta2 = fields.Many2one("boleta_ruta", string="Ruta")
    #origen_destino = fields.Char("Origen/Destino")
    precio = fields.Float("Precio")
    #totals
    precio_qq = fields.Float("Precio x qq.")
    total = fields.Float("Total")


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
        if self.tipo_ruta == False:
            self.costo_ruta = 0

    name = fields.Char("Ruta")
    codigo = fields.Char("Código")
    tipo_ruta = fields.Selection([('corta', 'Ruta Corta'), ('larga', 'Ruta Larga'), ('bcorta', 'Barco Corto'), ('blargo', 'Barco Largo')], string="Tipo Ruta")
    costo_ruta = fields.Float("Precio")
    productos = fields.One2many("boleta_ruta_producto", "ruta")