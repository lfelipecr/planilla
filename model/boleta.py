# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime


class boleta(models.Model):
    _name = "boleta"
    _description = "Boleta"

    @api.onchange("producto", "peso_kg", "ruta")
    def change_ruta(self):
        self.precio = self.ruta.costo_ruta
        self.peso_qq = self.peso_kg / 46

        self.precio_qq = 0
        if len(self.producto):
            for line in self.ruta.productos:
                if line.id == self.producto.id:
                    self.precio_qq = line.costo_viaje

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
    #origen_destino = fields.Char("Origen/Destino")
    precio = fields.Float("Precio")
    #totals
    precio_qq = fields.Float("Precio x qq.")
    total = fields.Float("Total")