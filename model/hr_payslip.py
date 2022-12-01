# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class hr_payslip_inherit_planilla(models.Model):
    _inherit = "hr.payslip"

    @api.onchange("cant_cortos")
    def change_cortos(self):
        if len(self.contract_id):
            self.costo_cortos = self.contract_id.corto * self.cant_cortos
        else:
            self.costo_cortos = 0

    @api.onchange("cant_largos")
    def change_largos(self):
        if len(self.contract_id):
            self.costo_largos = self.contract_id.largo * self.cant_largos
        else:
            self.costo_largos = 0

    @api.onchange("cant_bcortos")
    def change_bcortos(self):
        if len(self.contract_id):
            self.costo_bcortos = self.contract_id.barco_corto * self.cant_bcortos
        else:
            self.costo_bcortos = 0

    @api.onchange("cant_blargos")
    def change_blargos(self):
        if len(self.contract_id):
            self.costo_blargos = self.contract_id.barco_largo * self.cant_blargos
        else:
            self.costo_blargos = 0

    @api.onchange("cant_locos")
    def change_locos(self):
        if len(self.contract_id):
            self.costo_locos = self.contract_id.locos * self.cant_locos
        else:
            self.costo_locos = 0

    @api.onchange("cant_noches")
    def change_noches(self):
        if len(self.contract_id):
            self.costo_noches = self.contract_id.noches * self.cant_noches
        else:
            self.costo_noches = 0

    @api.onchange("cant_feriados")
    def change_feriados(self):
        if len(self.contract_id):
            self.costo_feriados = self.contract_id.feriados * self.cant_feriados
        else:
            self.costo_feriados = 0

    codigo = fields.Integer(related="employee_id.codigo", string="Código Empleado")
    semana_pagar = fields.Integer("Semana a Pagar")
    saldo_prestamo = fields.Float("Saldo Préstamo")
    fecha_pago = fields.Date("Fecha Pago")

    #viajes
    cant_cortos = fields.Integer("Cant. Cortos")
    costo_cortos = fields.Float("Costo Cortos")
    cant_largos = fields.Integer("Cant. Largos")
    costo_largos = fields.Float("Costo Largos")
    cant_bcortos = fields.Integer("Cant. Barco Cortos")
    costo_bcortos = fields.Float("Costo Barco Cortos")
    cant_blargos = fields.Integer("Cant. Barco Largos")
    costo_blargos = fields.Float("Costo Barco Largos")

    cant_locos = fields.Integer("Cant. Locos")
    costo_locos = fields.Float("Costo Locos")
    cant_noches = fields.Integer("Cant. Noches")
    costo_noches = fields.Float("Costo Noches")
    cant_feriados = fields.Integer("Cant. Feriados")
    costo_feriados = fields.Float("Costo Feriados")

    carga = fields.Float("Carga/Descarga")
    bonific = fields.Float("Bonific.")

    #deducciones
    deduc_obrera = fields.Float("Deduc. Obrera")
    prestamo = fields.Float("Préstamo")
    ahorro = fields.Float("Ahorro")
    otras_deduc = fields.Float("Otras Deduc.")