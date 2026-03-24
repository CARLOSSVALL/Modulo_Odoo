# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LostObject(models.Model):
    _name = 'lost.object'
    _description = 'Objeto Perdido'
    _rec_name = 'name'
    _order = 'registration_date desc, id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Nombre del Objeto',
        required=True,
        tracking=True,
    )
    description = fields.Text(
        string='Descripción',
        help='Descripción detallada del objeto perdido',
    )
    photo = fields.Binary(
        string='Foto',
        attachment=True,
    )
    photo_filename = fields.Char(string='Nombre del archivo de foto')
    category_id = fields.Many2one(
        comodel_name='lost.object.category',
        string='Categoría',
        ondelete='set null',
        tracking=True,
    )
    registration_date = fields.Date(
        string='Fecha de Registro',
        required=True,
        default=fields.Date.today,
        tracking=True,
    )
    state = fields.Selection(
        selection=[
            ('lost', 'Perdido'),
            ('delivered', 'Entregado'),
        ],
        string='Estado',
        default='lost',
        required=True,
        tracking=True,
        copy=False,
    )
    student_id = fields.Many2one(
        comodel_name='school.student',
        string='Alumno que lo Recogió',
        readonly=True,
        ondelete='set null',
        tracking=True,
        copy=False,
    )

    # -------------------------------------------------------------------------
    # Action: Publish (Publicar y Volver)
    # -------------------------------------------------------------------------
    def action_publish(self):
        """Al darle a publicar, Odoo guarda y redirige de vuelta a la vista."""
        self.ensure_one()
        # Le decimos a Odoo que nos devuelva a la pantalla principal
        action = self.env.ref('school_lost_found.action_lost_object').read()[0]
        return action

    # -------------------------------------------------------------------------
    # Action: Open Deliver Wizard
    # -------------------------------------------------------------------------
    def action_open_deliver_wizard(self):
        """Abre el wizard para entregar el objeto a un alumno."""
        self.ensure_one()
        if self.state != 'lost':
            raise ValidationError('Este objeto ya ha sido entregado.')
        return {
            'type': 'ir.actions.act_window',
            'name': 'Entregar Objeto',
            'res_model': 'lost.object.deliver.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_lost_object_id': self.id,
            },
        }

    # -------------------------------------------------------------------------
    # Compute / Constraints
    # -------------------------------------------------------------------------
    @api.constrains('state', 'student_id')
    def _check_delivered_student(self):
        for record in self:
            if record.state == 'delivered' and not record.student_id:
                raise ValidationError(
                    'Un objeto en estado "Entregado" debe tener un alumno asignado.'
                )
