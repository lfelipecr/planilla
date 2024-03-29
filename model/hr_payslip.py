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
        self.change_feriados()

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
    cant_otros = fields.Integer("Cant. Otros")
    costo_otros = fields.Float("Costo Otros")

    cant_locos = fields.Integer("Cant. Locos")
    costo_locos = fields.Float("Costo Locos")
    cant_noches = fields.Integer("Cant. Noches")
    costo_noches = fields.Float("Costo Noches")
    cant_feriados = fields.Integer("Cant. Domingos") #Este campo es donde se guarda los datos de los domingos trabajados
    costo_feriados = fields.Float("Costo Domingos")

    otros_viajes = fields.Float("Otros Viajes")

    carga = fields.Float("Carga/Descarga")
    bonific = fields.Float("Bonific.")
    reintegros = fields.Float("Reintegros")
    feriados  = fields.Float("Feriados") #aqui se guarda realmente la informacion de los feriados trabajados, se creo el 20/10/2023

    #deducciones
    deduc_obrera = fields.Float("Deduc. Obrera")
    prestamo = fields.Float("Préstamo")
    ahorro = fields.Float("Ahorro")
    otras_deduc = fields.Float("Otras Deduc.")
    adelantos = fields.Float("Adelantos")

    total_neto = fields.Float("Neto", compute="get_neto")
    total_viaticos = fields.Float("Viáticos", compute="get_viaticos")
    total_pagar = fields.Float("Total", compute="get_total")


class hr_payslip_report(models.Model):
    _name = "hr_payslip_report"

    def get_company(self):
        return self.env.company.id

    def obtener_planilla(self):
        self.env['hr_payslip_report_line'].search([('report', '=', self.id)]).unlink()
        planillas = self.env['hr.payslip'].search([('date_from', '>=', self.date_from), ('date_to', '<=', self.date_to)])
        for planilla in planillas:
            salario = 0
            total = 0
            for line in planilla.line_ids:
                if line.code == "GROSS":
                    salario = line.total
                #if line.code == "TOTAL":
                #    total = line.total
            depositado = salario + planilla.feriados + planilla.bonific - planilla.otras_deduc - planilla.ahorro - planilla.prestamo - planilla.deduc_obrera
            self.env['hr_payslip_report_line'].create({
                'name': planilla.employee_id.id,
                'salario': salario,
                'prestamos': planilla.prestamo,
                'ahorro': planilla.ahorro,
                'bonif': planilla.bonific,
                'depositado': depositado,
                'feriados' : planilla.feriados,
                'zapatos': planilla.otras_deduc,
                'deduccion': planilla.deduc_obrera,
                'report': self.id,
            })

        self.env['hr_payslip_report_gasto'].search([('report', '=', self.id)]).unlink()
        gastos = self.env['hr.payslip'].search([('date_from', '>=', self.date_from), ('date_to', '<=', self.date_to)])
        for gasto in gastos:
            """
            cant_largos = gasto.cant_largos + gasto.cant_blargos
            costo_largos = gasto.costo_largos + gasto.costo_blargos

            cant_blargos
            viajes_cortos = gasto.cant_cortos + gasto.cant_bcortos
            monto_cortos = gasto.costo_cortos + gasto.costo_bcortos
            """

            self.env['hr_payslip_report_gasto'].create({
                'name': gasto.employee_id.id,
                'viajes_largos': gasto.cant_largos,
                'monto_largos': gasto.costo_largos,
                'viajes_barco_largos': gasto.cant_blargos,
                'monto_barco_largos': gasto.costo_blargos,
                'viajes_cortos': gasto.cant_cortos,
                'monto_cortos': gasto.costo_cortos,
                'viajes_barco_cortos': gasto.cant_bcortos,
                'monto_barco_cortos': gasto.costo_bcortos,
                'bodega_adm': gasto.costo_otros,
                'otros_viajes': gasto.otros_viajes,
                'peajes': gasto.reintegros,
                'noches': gasto.costo_noches,
                'feriados' : gasto.costo_feriados,
                'costo_locos': gasto.costo_locos,
                'carga': gasto.carga,
                'adelanto_barco': "(" + str(gasto.adelantos) + ")",
                'adelanto': gasto.adelantos,
                'pago_total': (gasto.costo_largos + gasto.costo_blargos + gasto.costo_cortos + gasto.costo_bcortos + gasto.costo_noches +
                               gasto.costo_feriados + gasto.carga  + gasto.costo_otros + gasto.otros_viajes + gasto.costo_locos + gasto.reintegros) - gasto.adelantos,
                'report': self.id,
            })

    def planilla_to_excel(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Planilla semanal',
            'view_mode': 'tree',
            'res_model': 'hr_payslip_report_line',
            'target': 'current',
        }

    def gastos_to_excel(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Gastos semanal',
            'view_mode': 'tree',
            'res_model': 'hr_payslip_report_gasto',
            'target': 'current',
        }

    name = fields.Char("Name")
    company = fields.Many2one("res.company", string="Company", default=get_company)
    date_from = fields.Date("De")
    date_to = fields.Date("A")
    planillas = fields.One2many("hr_payslip_report_line", "report")
    gastos = fields.One2many("hr_payslip_report_gasto", "report")


class hr_payslip_report_line(models.Model):
    _name = "hr_payslip_report_line"
    _order = "name asc"

    name = fields.Many2one("hr.employee", string="Empleado")
    cedula = fields.Char(related="name.identification_id")
    oficio = fields.Many2one("hr.job", related="name.job_id")
    salario = fields.Float("Salario Bruto")
    prestamos = fields.Float("Prestamo")
    ahorro = fields.Float("Ahorro")
    bonif = fields.Float("Bonificaciones")
    zapatos = fields.Float("Zapatos")
    adelantos = fields.Float("Adelantos")
    deduccion = fields.Float("Deduccion Obrera")
    feriados  = fields.Float("Feriados")
    depositado = fields.Float("Pago Total")
    report = fields.Many2one("hr_payslip_report")


class hr_payslip_report_gasto(models.Model):
    _name = "hr_payslip_report_gasto"
    _order = "name asc"

    name = fields.Many2one("hr.employee", string="Empleado")
    viajes_largos = fields.Integer("Viajes largos")
    monto_largos = fields.Float("Monto")
    viajes_barco_largos = fields.Integer("Barco largos")
    monto_barco_largos = fields.Float("Monto")
    viajes_cortos = fields.Integer("Viajes cortos")
    monto_cortos = fields.Float("Monto")
    viajes_barco_cortos = fields.Integer("Barco cortos")
    monto_barco_cortos = fields.Float("Monto")
    otros_viajes = fields.Float("Otros Viajes")
    costo_locos = fields.Float("Costo Locos")
    bodega_adm = fields.Float("Bodega adm")
    peajes = fields.Float("Peajes/Fact")
    noches = fields.Float("Noches")
    feriados = fields.Float("Domingos")
    carga = fields.Float("Carga/Descarga")
    adelanto_barco = fields.Char("Adelanto barco")
    adelanto = fields.Float("Adelanto")
    pago_total = fields.Float("Pago total")
    monto_feriados = fields.Float("Feriados")
    report = fields.Many2one("hr_payslip_report")
