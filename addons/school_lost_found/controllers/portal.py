# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class SchoolLostFoundPortal(http.Controller):
    """
    Controlador público para el portal web de objetos perdidos.
    Ruta /objetos-perdidos:
        - GET:  Muestra el formulario de acceso por NIA.
        - POST: Valida el NIA; si es correcto, muestra la galería de objetos perdidos.
    """

    @http.route('/objetos-perdidos', type='http', auth='public', website=True, methods=['GET'])
    def lost_found_gateway(self, **kwargs):
        """Paso 1: Muestra el formulario de acceso con el campo NIA."""
        return request.render(
            'school_lost_found.portal_gateway_template',
            {
                'error': None,
                'page_title': 'Objetos Perdidos - Acceso',
            }
        )

    @http.route('/objetos-perdidos', type='http', auth='public', website=True, methods=['POST'], csrf=True)
    def lost_found_gallery(self, nia=None, **kwargs):
        """
        Paso 2: Valida el NIA enviado.
        - Si no existe: recarga el formulario con error.
        - Si existe: renderiza la galería de objetos perdidos.
        """
        nia = (nia or '').strip()

        if not nia:
            return request.render(
                'school_lost_found.portal_gateway_template',
                {
                    'error': 'Por favor, introduce tu NIA.',
                    'page_title': 'Objetos Perdidos - Acceso',
                }
            )

        student = request.env['school.student'].sudo().search(
            [('nia', '=', nia)], limit=1
        )

        if not student:
            return request.render(
                'school_lost_found.portal_gateway_template',
                {
                    'error': f'El NIA "{nia}" no está registrado. Contacta con conserjería.',
                    'page_title': 'Objetos Perdidos - Acceso',
                }
            )

        # Obtener objetos perdidos (solo los que siguen Sin entregar)
        lost_objects = request.env['lost.object'].sudo().search([
            ('state', '=', 'lost'),
        ], order='registration_date desc')

        return request.render(
            'school_lost_found.portal_gallery_template',
            {
                'student': student,
                'lost_objects': lost_objects,
                'page_title': f'Objetos Perdidos - Hola, {student.name}',
            }
        )
