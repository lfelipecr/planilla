# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class hr_payslip_inherit_planilla(models.Model):
    _inherit = "hr.payslip"

    @api.onchange("cant_cortos")
    def change_cortos(self):
        rutas = self.env['rutas'].search([], limit=1)
        self.costo_cortos = rutas.corto * self.cant_cortos

    @api.onchange("cant_largos")
    def change_largos(self):
        rutas = self.env['rutas'].search([], limit=1)
        self.costo_largos = rutas.largo * self.cant_largos

    @api.onchange("cant_bcortos")
    def change_bcortos(self):
        rutas = self.env['rutas'].search([], limit=1)
        self.costo_bcortos = rutas.barco_corto * self.cant_bcortos

    @api.onchange("cant_blargos")
    def change_blargos(self):
        rutas = self.env['rutas'].search([], limit=1)
        self.costo_blargos = rutas.barco_largo * self.cant_blargos

    @api.onchange("cant_otros")
    def change_otros(self):
        rutas = self.env['rutas'].search([], limit=1)
        self.costo_otros = rutas.otras_rutas * self.cant_otros

    @api.onchange("cant_locos")
    def change_locos(self):
        viaticos = self.env['viaticos'].search([], limit=1)
        self.costo_locos = viaticos.locos * self.cant_locos

    @api.onchange("cant_noches")
    def change_noches(self):
        viaticos = self.env['viaticos'].search([], limit=1)
        self.costo_noches = viaticos.noches * self.cant_noches

    @api.onchange("cant_feriados")
    def change_feriados(self):
        viaticos = self.env['viaticos'].search([], limit=1)
        self.costo_feriados = viaticos.feriados * self.cant_feriados

    def get_neto(self):
        for rec in self:
            rec.total_neto = 0
            for line in rec.line_ids:
                if line.code == "NET":
                    rec.total_neto = line.total

    def get_viaticos(self):
        for rec in self:
            rec.total_viaticos = 0
            for line in rec.line_ids:
                if line.code == "VIAT":
                    rec.total_viaticos = line.total

    def get_total(self):
        for rec in self:
            rec.total_pagar = 0
            for line in rec.line_ids:
                if line.code == "TOTAL":
                    rec.total_pagar = line.total

    def get_boletas(self):
        cortos = 0
        largos = 0
        bcortos = 0
        blargos = 0
        otras = 0
        boletas = self.env['boleta'].search([('date', '>=', self.date_from), ('date', '<=', self.date_to), ('chofer', '=', self.employee_id.id)])

        for boleta in boletas:
            if boleta.ruta2.tipo_ruta == "corta":
                cortos = cortos + 1
            if boleta.ruta2.tipo_ruta == "larga":
                largos = largos + 1
            if boleta.ruta2.tipo_ruta == "bcorta":
                bcortos = bcortos + 1
            if boleta.ruta2.tipo_ruta == "blargo":
                blargos = blargos + 1
            if boleta.ruta2.tipo_ruta == "otras":
                otras = otras + 1

        self.cant_cortos = cortos
        self.change_cortos()
        self.cant_largos = largos
        self.change_largos()
        self.cant_bcortos = bcortos
        self.change_bcortos()
        self.cant_blargos = blargos
        self.change_blargos()
        self.cant_otros = otras
        self.change_otros()

    codigo = fields.Integer(related="employee_id.codigo", string="C??digo Empleado")
    semana_pagar = fields.Integer("Semana a Pagar")
    saldo_prestamo = fields.Float("Saldo Pr??stamo")
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
    cant_otros = fields.Integer("Cant. Otros")
    costo_otros = fields.Float("Costo Otros")

    cant_locos = fields.Integer("Cant. Locos")
    costo_locos = fields.Float("Costo Locos")
    cant_noches = fields.Integer("Cant. Noches")
    costo_noches = fields.Float("Costo Noches")
    cant_feriados = fields.Integer("Cant. Feriados")
    costo_feriados = fields.Float("Costo Feriados")

    otros_viajes = fields.Float("Otros Viajes")

    carga = fields.Float("Carga/Descarga")
    bonific = fields.Float("Bonific.")
    reintegros = fields.Float("Reintegros")

    #deducciones
    deduc_obrera = fields.Float("Deduc. Obrera")
    prestamo = fields.Float("Pr??stamo")
    ahorro = fields.Float("Ahorro")
    otras_deduc = fields.Float("Otras Deduc.")
    adelantos = fields.Float("Adelantos")

    total_neto = fields.Float("Neto", compute="get_neto")
    total_viaticos = fields.Float("Vi??ticos", compute="get_viaticos")
    total_pagar = fields.Float("Total", compute="get_total")