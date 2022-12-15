# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class planilla_viaticos(models.Model):
    _name = "viaticos"
    _description = "viaticos"

    name = fields.Char("Nombre", default="Viáticos")
    feriados = fields.Float("Feriados")
    noches = fields.Float("Noches")
    locos = fields.Float("Locos")


class planilla_rutas(models.Model):
    _name = "rutas"
    _description = "rutas"

    name = fields.Char("Rutas", default="Rutas")
    corto = fields.Float("Ruta Corta")
    largo = fields.Float("Ruta Larga")
    barco_corto = fields.Float("Barco corto")
    barco_largo = fields.Float("Barco largo")
    otras_rutas = fields.Float("Otras rutas")