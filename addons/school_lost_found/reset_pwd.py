import sys
import odoo

print("Conectando con Odoo...")
odoo.tools.config.parse_config(['-d', 'Modu'])
print("Cargando registro...")
registry = odoo.registry('Modu')
with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    print("Buscando administrador...")
    admin = env['res.users'].search([('login', '=', 'admin')], limit=1)
    if admin:
        # Aquí asignamos la nueva contraseña segura. Odoo la encriptará mágicamente.
        admin.password = 'admin'
        env.cr.commit()
        print("¡CONTRASEÑA DEL ADMIN EXITO!")
    else:
        print("ERROR: No se encontró al admin")
