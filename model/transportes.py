# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class transportes_rutas_inherit_planilla(models.Model):
    _inherit = "transportes.rutas"

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

    tipo_ruta = fields.Selection([('corta', 'Ruta Corta'), ('larga', 'Ruta Larga'), ('bcorta', 'Barco Corto'), ('blargo', 'Barco Largo')], string="Tipo Ruta")
    costo_ruta = fields.Float("Precio")