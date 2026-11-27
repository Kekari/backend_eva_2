import json

from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings

from .models import Tablero, Tarea


class ListadosTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usuario = get_user_model().objects.create_user(username='test')
        cls.tablero = Tablero.objects.create(usuario=cls.usuario, titulo='Proyecto de prueba')
        cls.tarea = Tarea.objects.create(tablero=cls.tablero, titulo='Primera tarea')

    def setUp(self):
        self.client = Client(HTTP_HOST='127.0.0.1')
        self.client.force_login(self.usuario)

    def test_listados_con_tabla_tarjetas_y_datatables(self):
        for tipo, titulo in [('tableros', self.tablero.titulo), ('tareas', self.tarea.titulo)]:
            response = self.client.get(f'/tflow/grupo_{tipo}/listado_{tipo}')
            self.assertContains(response, titulo)
            self.assertContains(response, 'class="card h-100"')
            self.assertContains(response, 'js/datatables.js')
            self.assertContains(response, f'id="{tipo}"')

    def test_crear_tablero_asignado_a_usuario(self):
        response = self.client.post('/tflow/grupo_tableros/crear_tablero', {
            'usuario': self.usuario.pk, 'titulo': 'Nuevo', 'descripcion': 'Una idea', 'color': 'green',
        })
        self.assertRedirects(response, '/tflow/grupo_tableros/listado_tableros')
        self.assertTrue(Tablero.objects.filter(titulo='Nuevo', usuario=self.usuario).exists())

    def test_crear_tarea_asignada_a_tablero(self):
        response = self.client.post('/tflow/grupo_tareas/crear_tarea', {
            'tablero': self.tablero.pk, 'titulo': 'Nueva', 'descripcion': '', 'estado': 1,
        })
        self.assertRedirects(response, '/tflow/grupo_tareas/listado_tareas')
        self.assertTrue(Tarea.objects.filter(titulo='Nueva', tablero=self.tablero, estado=1).exists())

    def test_errores_no_guardan_datos_invalidos(self):
        response = self.client.post('/tflow/grupo_tableros/crear_tablero', {})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
        response = self.client.post('/tflow/grupo_tareas/crear_tarea', {'tablero': 9999, 'titulo': 'Invalida', 'estado': 9})
        self.assertTrue(response.context['form'].errors)
        self.assertFalse(Tarea.objects.filter(titulo='Invalida').exists())

    def test_csrf_y_cancelacion(self):
        client = Client(enforce_csrf_checks=True, HTTP_HOST='127.0.0.1')
        self.assertEqual(client.post('/tflow/grupo_tableros/crear_tablero', {}).status_code, 403)
        self.assertContains(self.client.get('/tflow/grupo_tableros/crear_tablero'), 'Cancelar')

    @override_settings(DEBUG=False)
    def test_inicio_api_y_404_originales(self):
        self.assertEqual(self.client.get('/').status_code, 200)
        self.assertEqual(self.client.get('/tflow/tableros/').status_code, 200)
        self.assertEqual(self.client.get('/tflow/tareas/').status_code, 200)
        self.assertContains(self.client.get('/ruta-inexistente/'), 'Esta página no está en el tablero.', status_code=404)

    def test_editar_y_eliminar_tablero(self):
        ruta = f'/tflow/grupo_tableros/editar_tablero/{self.tablero.pk}'
        response = self.client.get(ruta)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-api-method="PATCH"')
        self.assertContains(response, f'data-api-url="/tflow/tableros/{self.tablero.pk}/"')
        self.assertContains(response, 'js/tflow/tableros/api.js')
        response = self.client.post(ruta, {'usuario': self.usuario.pk, 'titulo': 'Editado', 'descripcion': '', 'color': 'green'})
        self.assertRedirects(response, '/tflow/grupo_tableros/listado_tableros')
        self.tablero.refresh_from_db()
        self.assertEqual(self.tablero.titulo, 'Editado')
        ruta = f'/tflow/grupo_tableros/eliminar_tablero/{self.tablero.pk}'
        response = self.client.get(ruta)
        self.assertContains(response, 'Cancelar')
        self.assertContains(response, 'data-api-method="DELETE"')
        self.assertTrue(Tablero.objects.filter(pk=self.tablero.pk).exists())
        self.assertEqual(self.client.delete(ruta).status_code, 405)
        self.assertRedirects(self.client.post(ruta), '/tflow/grupo_tableros/listado_tableros')
        self.assertFalse(Tarea.objects.filter(pk=self.tarea.pk).exists())

    def test_api_tablero_acepta_patch_y_delete(self):
        client = Client(enforce_csrf_checks=True, HTTP_HOST='127.0.0.1')
        client.force_login(self.usuario)
        detalle = f'/tflow/tableros/{self.tablero.pk}/'
        client.get(f'/tflow/grupo_tableros/editar_tablero/{self.tablero.pk}')
        csrf_token = client.cookies['csrftoken'].value

        response = client.patch(
            detalle,
            json.dumps({'titulo': 'Actualizado por PATCH'}),
            content_type='application/json',
            HTTP_X_CSRFTOKEN=csrf_token,
        )
        self.assertEqual(response.status_code, 200)
        self.tablero.refresh_from_db()
        self.assertEqual(self.tablero.titulo, 'Actualizado por PATCH')

        response = client.delete(detalle, HTTP_X_CSRFTOKEN=csrf_token)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Tablero.objects.filter(pk=self.tablero.pk).exists())

    def test_editar_y_eliminar_tarea(self):
        ruta = f'/tflow/grupo_tareas/editar_tarea/{self.tarea.pk}'
        response = self.client.post(ruta, {'tablero': self.tablero.pk, 'titulo': 'Actualizada', 'descripcion': '', 'estado': 2})
        self.assertRedirects(response, '/tflow/grupo_tareas/listado_tareas')
        self.tarea.refresh_from_db()
        self.assertEqual(self.tarea.estado, 2)
        ruta = f'/tflow/grupo_tareas/eliminar_tarea/{self.tarea.pk}'
        self.assertEqual(self.client.get(ruta).status_code, 200)
        self.assertRedirects(self.client.post(ruta), '/tflow/grupo_tareas/listado_tareas')
        self.assertTrue(Tablero.objects.filter(pk=self.tablero.pk).exists())


class SesionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usuario = get_user_model().objects.create_user('ana', email='ana@example.com', password='ClaveSegura_79243')

    def setUp(self):
        self.client = Client(HTTP_HOST='127.0.0.1')

    def test_registro_y_bienvenida(self):
        response = self.client.post('/registro/', {
            'username': 'nueva', 'email': 'nueva@example.com',
            'password1': 'OtraClaveSegura_81243', 'password2': 'OtraClaveSegura_81243',
        })
        self.assertRedirects(response, '/')
        user = get_user_model().objects.get(username='nueva')
        self.assertTrue(user.check_password('OtraClaveSegura_81243'))
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)
        self.assertNotIn('mensaje_bienvenida', self.client.session)

    def test_registro_invalido(self):
        response = self.client.post('/registro/', {'username': 'ana', 'password1': '1', 'password2': '2'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_login_logout_y_redireccion(self):
        response = self.client.post('/login/', {'username': 'ana', 'password': 'incorrecta'})
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertEqual(self.client.post('/login/', {'username': 'ana', 'password': 'ClaveSegura_79243'}).status_code, 302)
        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(self.client.get('/logout/').status_code, 405)
        self.assertEqual(self.client.post('/logout/').status_code, 302)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_acceso_protegido_y_configuracion_sesion(self):
        from django.conf import settings
        self.assertEqual(settings.SESSION_COOKIE_AGE, 3600)
        self.assertTrue(settings.SESSION_EXPIRE_AT_BROWSER_CLOSE)
        self.assertEqual(settings.SESSION_ENGINE, 'django.contrib.sessions.backends.db')
        for ruta in ['/tflow/grupo_tableros/listado_tableros', '/tflow/grupo_tareas/crear_tarea']:
            self.assertEqual(self.client.get(ruta).status_code, 302)
        for ruta in ['/tflow/tableros/', '/tflow/tareas/']:
            self.assertEqual(self.client.get(ruta).status_code, 403)

    def test_csrf(self):
        client = Client(enforce_csrf_checks=True, HTTP_HOST='127.0.0.1')
        self.assertEqual(client.post('/login/', {}).status_code, 403)
        self.assertEqual(client.post('/registro/', {}).status_code, 403)
        client.force_login(self.usuario)
        self.assertEqual(client.post('/logout/').status_code, 403)
        self.assertEqual(client.post('/tflow/tableros/', {'titulo': 'Sin token'}).status_code, 403)

    def test_recuperacion_y_cambio_password(self):
        from django.core import mail
        self.assertContains(self.client.get('/accounts/password_reset/'), 'Durante el desarrollo')
        response = self.client.post('/accounts/password_reset/', {'email': 'ana@example.com'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('/accounts/reset/', mail.outbox[0].body)
        import re
        enlace = re.search(r'http://[^\s]+(/accounts/reset/[^\s]+)', mail.outbox[0].body).group(1)
        response = self.client.get(enlace, follow=True)
        self.assertTrue(response.context['validlink'])
        confirmar = response.request['PATH_INFO']
        response = self.client.post(confirmar, {
            'new_password1': 'Restablecida_93457', 'new_password2': 'Restablecida_93457',
        })
        self.assertEqual(response.status_code, 302)
        self.usuario.refresh_from_db()
        self.assertTrue(self.usuario.check_password('Restablecida_93457'))
        self.client.force_login(self.usuario)
        response = self.client.post('/accounts/password_change/', {
            'old_password': 'Restablecida_93457', 'new_password1': 'CambioSeguro_81427',
            'new_password2': 'CambioSeguro_81427',
        })
        self.assertEqual(response.status_code, 302)
        self.usuario.refresh_from_db()
        self.assertTrue(self.usuario.check_password('CambioSeguro_81427'))
