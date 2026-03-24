# -*- coding: utf-8 -*-
from odoo import models, fields, api


class LostObjectCategory(models.Model):
    _name = 'lost.object.category'
    _description = 'Categoría de Objeto Perdido'
    _rec_name = 'name'
    _order = 'name asc'

    name = fields.Char(
        string='Nombre',
        required=True,
        translate=True,
    )
    active = fields.Boolean(
        string='Activo',
        default=True,
    )
    object_count = fields.Integer(
        string='Nº de Objetos',
        compute='_compute_object_count',
        store=True,
    )
    lost_object_ids = fields.One2many(
        comodel_name='lost.object',
        inverse_name='category_id',
        string='Objetos',
    )

    @api.depends('lost_object_ids')
    def _compute_object_count(self):
        for record in self:
            record.object_count = len(record.lost_object_ids)

    _sql_constraints = [
        (
            'name_unique',
            'UNIQUE(name)',
            'Ya existe una categoría con ese nombre.'
        ),
    ]
