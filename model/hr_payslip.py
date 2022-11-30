# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class hr_payslip_inherit_planilla(models.Model):
    _inherit = "hr.payslip"

    codigo = fields.Integer(related="employee_id.codigo", string="Código Empleado")
    semana_pagar = fields.Integer("Semana a Pagar")
    saldo_prestamo = fields.Float("Saldo Préstamo")
    fecha_pago = fields.Date("Fecha Pago")