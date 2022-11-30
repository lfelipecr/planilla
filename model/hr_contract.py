# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class hr_contract_inherit_planilla(models.Model):
    _inherit = "hr.contract"

    tipo_salario = fields.Selection([('horas', 'Por Horas'), ('fijo', 'Fijo')], string="Tipo Salario")
    parametros_planilla = fields.Boolean("Parametros de planilla")
    parametros_viaje = fields.Boolean("Parametros de viaje")

    #planilla
    feriados = fields.Float("Feriados")
    noches = fields.Float("Noches")
    locos = fields.Float("Locos")

    #viajes
    corto = fields.Float("Ruta Corta")
    largo = fields.Float("Ruta Larga")
    barco_corto = fields.Float("Barco corto")
    barco_largo = fields.Float("Barco largo")