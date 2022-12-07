# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime


class productos_boleta(models.Model):
    _inherit = 'product.template'

    costo_viaje = fields.Float(string='Costo viaje')