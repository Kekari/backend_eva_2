# TaskFlow

## 1. Descargar el proyecto

Abre una terminal y ejecuta:

```powershell
git clone https://github.com/Kekari/backend_eva_2.git
cd backend_eva_2
```

## 2. Crear y activar el ambiente virtual

El ambiente virtual mantiene las librerías del proyecto separadas de las de otros trabajos.

Para crearlo:

```powershell
python -m venv ambiente
```

Para activarlo, entra a la carpeta `Scripts` y ejecuta:

```powershell
cd ambiente\Scripts
.\Activate
```

Si PowerShell bloquea la activación, ejecuta este comando en esa misma carpeta y después vuelve a ejecutar `.\Activate`:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Luego vuelve a la carpeta principal del proyecto:

```powershell
cd..
cd..
```

## 3. Instalar las librerías

Con el ambiente activado, ejecuta:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

`requirements.txt` contiene las librerías y sus versiones.

## 4. Preparar MySQL

El archivo [scripts/configurar_mysql.sql](scripts/configurar_mysql.sql) contiene los comandos para:

- Crear la base de datos `tflow`.
- Crear el usuario MySQL `admin`.
- Darle permisos sobre la base de datos del proyecto.

Para usarlo desde phpMyAdmin:

1. Inicia MySQL y entra a phpMyAdmin con una cuenta administradora.
2. Abre el archivo SQL y cambia `CAMBIAR_ESTA_CLAVE` por la contraseña que quieras usar.
3. Copia su contenido en la pestaña **SQL** de phpMyAdmin y ejecútalo.

Si el usuario `admin` con host `%` ya existe, el script conserva su contraseña actual. En ese caso, usa esa contraseña en el siguiente paso.

El usuario MySQL permite que Django se conecte a la base de datos. Es distinto de los usuarios que aparecerán dentro de Django.

## 5. Crear las tablas con las migraciones

```powershell
python manage.py migrate
```

## 6. Cargar los datos iniciales

En una base de datos recién preparada, ejecuta este paso antes de crear el superusuario:

```powershell
python manage.py loaddata datos_iniciales
```

El archivo `tflow/fixtures/datos_iniciales.json` carga:

- Un usuario de prueba llamado `test`, con ID `1`.
- Un tablero llamado **Mi primer proyecto**, asignado a ese usuario.
- Tres tareas, una en cada estado.

El usuario `test` sirve para asignarle tableros desde la API.

## 7. Crear el superusuario de Django

Para poder entrar al administrador, ejecuta:

```powershell
python manage.py createsuperuser
```

Este superusuario sirve para administrar los datos desde Django. No es el usuario MySQL `admin` ni el usuario de prueba `test`.

## 8. Iniciar el proyecto

Ejecuta:

```powershell
python manage.py runserver
```

El servidor se inicia en el puerto **8000**.

| Dirección | Qué puedes revisar |
| --- | --- |
| http://127.0.0.1:8000/ | Página principal de TaskFlow |
| http://127.0.0.1:8000/tflow/ | Inicio de la API |
| http://127.0.0.1:8000/tflow/tableros/ | Lista y creación de tableros |
| http://127.0.0.1:8000/tflow/tareas/ | Lista y creación de tareas |

### Crear un tablero

Abre http://127.0.0.1:8000/tflow/tableros/. Al final de la página encontrarás el formulario de Django REST Framework.

Completa los campos, selecciona `test` como usuario y presiona **POST**. Si usas la pestaña **Raw data**, selecciona `application/json` y puedes enviar este ejemplo:

```json
{
  "usuario": 1,
  "titulo": "Proyecto de prueba",
  "descripcion": "Tablero para revisar el funcionamiento de la API.",
  "color": "purple"
}
```

### Crear una tarea

Abre http://127.0.0.1:8000/tflow/tareas/, completa el formulario y presiona **POST**.

Este ejemplo usa el tablero inicial con ID `1`. Para usar el que acabas de crear, cambia el valor de `tablero` por su ID:

```json
{
  "tablero": 1,
  "titulo": "Preparar la entrega",
  "descripcion": "Revisar los archivos del proyecto.",
  "estado": 0
}
```

### Consultar, modificar y eliminar

Para probar se puede ingresar a http://127.0.0.1:8000/tflow/tareas/1/.

- **GET** muestra los datos guardados.
- **PUT** permite enviar todos los campos editables para actualizar el registro.
- **PATCH** permite cambiar solo algunos campos. Por ejemplo, enviar `{"estado": 2}` cambia una tarea a Completado.
- **DELETE** elimina el registro seleccionado.

## 9. Página principal y error 404

La página principal es una demostración visual de TaskFlow. Permite crear tableros, agregar tareas, cambiar sus estados y eliminar los tableros creados.

`inicio.html` y `404.html` heredan el diseño de `base.html`.

Para probar el error 404, visita una ruta que no exista, por ejemplo http://127.0.0.1:8000/pagina-inexistente/. Aparecerá una página con el diseño de TaskFlow y un enlace para volver al inicio.

## 10. Comprobaciones finales

Si se modifican o crean nuevos modelos con los comandos se generan y aplican sus migraciones:

```powershell
python manage.py makemigrations
python manage.py migrate
```

Cuando termines de trabajar, puedes salir del ambiente virtual con:

```powershell
deactivate
```


## Listados y formularios web

Adaptados de las vistas y plantillas del proyecto de clases del profesor Erick Bailey Rebolledo: https://github.com/baileytorch/IEI_N4_C1.

- Tableros: http://127.0.0.1:8000/tflow/grupo_tableros/listado_tableros
- Agregar tablero: http://127.0.0.1:8000/tflow/grupo_tableros/crear_tablero
- Tareas: http://127.0.0.1:8000/tflow/grupo_tareas/listado_tareas
- Agregar tarea: http://127.0.0.1:8000/tflow/grupo_tareas/crear_tarea

Puedes entrar desde el enlace **Mantenimiento** de la página principal. Los listados muestran los datos en tablas y tarjetas. Usa **Buscar**, los encabezados para ordenar, el selector de cantidad de registros y la paginación de DataTables.

Para agregar un tablero, elige un usuario existente. Para agregar una tarea, elige un tablero existente. Completa los campos y pulsa **Guardar**; el registro se guarda en MySQL y vuelve al listado. **Cancelar** permite volver sin guardar.

Se utilizan ListView, CreateView, ModelForm y los mismos archivos de Bootstrap Flatly, jQuery y DataTables del profesor, guardados en `static/`. La API conserva sus rutas anteriores. Sobre la adaptación de los listados y la creación se completa el CRUD manual con edición y eliminación, además de las sesiones del punto 21 del README del profesor.

El modo de desarrollo está en `DEBUG = True`, igual que en la configuración actual del profesor, para que `python manage.py runserver` sirva los archivos estáticos en el puerto 8000. La plantilla 404 personalizada se conserva y se muestra al usar `DEBUG = False`.


## Registro, sesiones y CRUD completo

- Crear cuenta: http://127.0.0.1:8000/registro/
- Iniciar sesión: http://127.0.0.1:8000/login/
- Recuperar contraseña: http://127.0.0.1:8000/accounts/password_reset/
- Cambiar contraseña: usa el enlace del menú después de iniciar sesión.

Al registrarte se guarda tu cuenta de Django y se inicia la sesión. Los listados, formularios y la API requieren una sesión activa. Para salir, usa **Cerrar sesión**: ese botón envía un formulario protegido y limpia la sesión.

Las sesiones se guardan en la base de datos, duran una hora y su cookie expira al cerrar el navegador. El mantenimiento continúa siendo compartido entre las cuentas autenticadas, como en la aplicación de clases; no se añadieron reglas particulares de propiedad.

Las tablas de tableros y tareas incluyen **Editar** y **Eliminar**. La eliminación pide confirmación y solo se ejecuta al enviar el formulario. Al eliminar un tablero también se eliminan sus tareas.

La recuperación usa el correo de la cuenta. En desarrollo, el enlace aparece en la terminal donde se ejecuta Django; no se envían correos reales. Los usuarios anteriores sin correo pueden completarlo desde el administrador. Un envío real necesitaría configurar un servidor de correo.

La pantalla principal conserva los tableros de demostración del navegador. Para crear o modificar los registros de MySQL usa **Mantenimiento**. El antiguo acceso simulado de esa pantalla se reemplazó por el inicio de sesión real.

Para ejecutar las pruebas sin tocar MySQL ni avanzar sus ID:

```powershell
python manage.py test --settings=drf.test_settings
```

El detalle por archivo está en [CAMBIOS_README.md](CAMBIOS_README.md).
