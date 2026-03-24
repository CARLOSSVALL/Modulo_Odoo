# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LostObjectDeliverWizard(models.TransientModel):
    _name = 'lost.object.deliver.wizard'
    _description = 'Wizard: Entregar Objeto Perdido'

    lost_object_id = fields.Many2one(
        comodel_name='lost.object',
        string='Objeto Perdido',
        required=True,
        readonly=True,
    )
    nia = fields.Char(
        string='NIA del Alumno',
        required=True,
        help='Introduce el Número de Identificación del Alumno que recoge el objeto.',
    )
    student_id = fields.Many2one(
        comodel_name='school.student',
        string='Alumno Encontrado',
        readonly=True,
    )

    @api.onchange('nia')
    def _onchange_nia(self):
        """Búsqueda en tiempo real del alumno mientras se escribe el NIA."""
        self.student_id = False
        if self.nia:
            student = self.env['school.student'].search(
                [('nia', '=', self.nia.strip())], limit=1
            )
            if student:
                self.student_id = student.id

    def action_confirm_delivery(self):
        """
        Valida el NIA, busca el alumno y actualiza el objeto perdido.
        Lanza ValidationError si el alumno no existe.
        """
        self.ensure_one()
        if not self.nia or not self.nia.strip():
            raise ValidationError('Por favor, introduce un NIA válido.')

        student = self.env['school.student'].search(
            [('nia', '=', self.nia.strip())], limit=1
        )
        if not student:
            raise ValidationError(
                f'No se encontró ningún alumno con el NIA "{self.nia.strip()}". '
                f'Verifica el número e inténtalo de nuevo.'
            )

        lost_object = self.lost_object_id
        if lost_object.state == 'delivered':
            raise ValidationError('Este objeto ya fue entregado anteriormente.')

        lost_object.write({
            'state': 'delivered',
            'student_id': student.id,
        })

        # Mostrar notificación de éxito y cerrar wizard
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': '¡Entrega Realizada!',
                'message': f'El objeto "{lost_object.name}" fue entregado a {student.name} (NIA: {student.nia}).',
                'type': 'success',
                'sticky': False,
            },
        }
