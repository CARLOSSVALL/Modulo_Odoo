# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SchoolStudent(models.Model):
    _name = 'school.student'
    _description = 'Alumno del Centro Escolar'
    _rec_name = 'name'
    _order = 'name asc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    first_name = fields.Char(
        string='Nombre',
        required=True,
        tracking=True,
    )
    last_name = fields.Char(
        string='Apellidos',
        required=True,
        tracking=True,
    )
    name = fields.Char(
        string='Nombre Completo',
        compute='_compute_name',
        store=True,
    )
    nia = fields.Char(
        string='NIA',
        required=True,
        copy=False,
        help='Número de Identificación del Alumno (único)',
    )
    lost_object_ids = fields.One2many(
        comodel_name='lost.object',
        inverse_name='student_id',
        string='Objetos Entregados',
        readonly=True,
    )
    lost_object_count = fields.Integer(
        string='Nº Objetos Entregados',
        compute='_compute_lost_object_count',
        store=True,
    )

    _sql_constraints = [
        (
            'nia_unique',
            'UNIQUE(nia)',
            'El NIA debe ser único. Ya existe un alumno con ese NIA.'
        ),
    ]

    @api.depends('lost_object_ids')
    def _compute_lost_object_count(self):
        for record in self:
            record.lost_object_count = len(record.lost_object_ids)

    @api.constrains('nia')
    def _check_nia(self):
        for record in self:
            if record.nia and not record.nia.strip():
                raise ValidationError('El NIA no puede estar vacío.')
            if record.nia and not record.nia.isdigit():
                raise ValidationError('El NIA solo puede contener números enteros.')

    @api.depends('first_name', 'last_name')
    def _compute_name(self):
        for record in self:
            parts = []
            if record.first_name:
                parts.append(record.first_name)
            if record.last_name:
                parts.append(record.last_name)
            record.name = " ".join(parts) if parts else "Nuevo Alumno"

    def action_save_student(self):
        """Botón Agregar Alumno. Odoo valida los campos nativamente."""
        self.ensure_one()
        return self.env.ref('school_lost_found.action_school_student').read()[0]
