# Registro de cambios — completar el README del profesor

Fecha: 15 de noviembre de 2026.
Referencia: README de baileytorch/IEI_N4_C1, sobre la adaptación de TaskFlow que ya tenía tablas, tarjetas, búsqueda, paginación y formularios de creación.

## Qué se completó

- **Punto 20, CRUD manual:** edición y eliminación de tableros y tareas, además de los listados y creación existentes. Se reutilizaron las vistas basadas en clase y formularios de Django. Este apartado de la guía solo tiene el título; se completa con las cuatro operaciones de CRUD sobre nuestros modelos.
- **Punto 21, sesiones:** registro, inicio y cierre de sesión, acceso protegido, mensajes, un dato de bienvenida en la sesión y configuración de duración y almacenamiento.
- **Herramientas de autenticación incluidas en la guía:** rutas de Django para cambiar y recuperar la contraseña, con sus plantillas adaptadas a TaskFlow.

## Archivos de configuración y lógica

| Archivo | Qué se cambió | Qué hace |
| --- | --- | --- |
| `drf/settings.py` | Redirecciones de acceso y salida; duración de 3600 segundos; expiración al cerrar el navegador; sesiones en la base de datos; prioridad de plantillas de TaskFlow | Define el comportamiento de las sesiones y evita que recuperación de contraseña cargue el diseño del administrador de Django |
| `drf/urls.py` | Rutas `accounts/`, `login/`, `logout/` y `registro/` | Conecta las herramientas nativas de autenticación y el formulario de registro |
| `tflow/forms.py` | Formulario `RegistroForm`, basado en `UserCreationForm`, con correo | Crea cuentas con contraseña cifrada y validación de Django; el correo permite recuperar la contraseña. Los formularios de tablero y tarea se conservan |
| `tflow/views.py` | Vista de registro; bienvenida guardada y retirada de la sesión; protección de listados y formularios; permisos de sesión en la API; `UpdateView` y `DeleteView` | Permite registrarse e iniciar sesión automáticamente; exige acceso para mantenimiento y API; guarda cambios y elimina después de confirmar |
| `tflow/urls.py` | Rutas de editar y eliminar para ambos modelos | Permite abrir las nuevas operaciones desde sus tablas |
| `drf/test_settings.py` | Configuración exclusiva para pruebas con SQLite en memoria | Impide que las pruebas automáticas creen cuentas o consuman ID en MySQL |
| `tflow/tests.py` | Pruebas de autenticación, registro, sesiones, recuperación/cambio de contraseña, protección y CRUD | Verifica el comportamiento sin cambiar los datos reales |

## Plantillas y estilos

| Archivo | Qué hace |
| --- | --- |
| `tflow/templates/base.html` | Carga los estilos de sesión y muestra los mensajes de Django |
| `tflow/templates/inicio.html` | Usa acceso real en el encabezado, elimina el popup de acceso simulado y conserva la demostración de tableros en el navegador |
| `tflow/templates/tflow/base_mantenimiento.html` | Añade los enlaces de cuenta y el formulario de cierre de sesión al menú existente |
| `tflow/templates/tflow/sesion.html` | Muestra el usuario, cambiar contraseña y cerrar sesión, o los enlaces de acceso y registro |
| `tflow/templates/tflow/tablero/listado_tableros.html` | Añade Editar y Eliminar a cada fila de tableros |
| `tflow/templates/tflow/tarea/listado_tareas.html` | Añade Editar y Eliminar a cada fila de tareas |
| `tflow/templates/tflow/tablero/editar_tablero.html` | Reutiliza el formulario de tablero para modificar un registro existente |
| `tflow/templates/tflow/tarea/editar_tarea.html` | Reutiliza el formulario de tarea para modificar un registro existente |
| `tflow/templates/tflow/tablero/eliminar_tablero.html` | Presenta la confirmación de eliminación de un tablero |
| `tflow/templates/tflow/tarea/eliminar_tarea.html` | Presenta la confirmación de eliminación de una tarea |
| `tflow/templates/tflow/confirmar_eliminar.html` | Formulario común con token CSRF, confirmación, aviso de cascada y botón Cancelar. Abrir esta pantalla no borra datos |
| `tflow/templates/registration/campos.html` | Presenta campos, ayuda y errores de los formularios de cuenta |
| `tflow/templates/registration/login.html` | Permite iniciar sesión y volver al lugar al que se intentaba acceder |
| `tflow/templates/registration/registro.html` | Formulario de creación de cuenta |
| `tflow/templates/registration/password_change_form.html` | Solicita la contraseña actual y la nueva |
| `tflow/templates/registration/password_change_done.html` | Confirma el cambio de contraseña |
| `tflow/templates/registration/password_reset_form.html` | Solicita el correo para recuperar acceso |
| `tflow/templates/registration/password_reset_done.html` | Confirma la recepción de la solicitud sin revelar si el correo existe |
| `tflow/templates/registration/password_reset_email.html` | Contenido del mensaje con el enlace de recuperación |
| `tflow/templates/registration/password_reset_subject.txt` | Asunto del mensaje de recuperación |
| `tflow/templates/registration/password_reset_confirm.html` | Permite elegir una contraseña nueva con un enlace válido y muestra un aviso si no lo es |
| `tflow/templates/registration/password_reset_complete.html` | Confirma la recuperación y ofrece volver al acceso |
| `static/css/sesion.css` | Ajusta el menú de cuenta, los mensajes y los formularios sin cambiar las librerías visuales del profesor |
| `README.md` | Documenta las nuevas rutas, la necesidad de iniciar sesión y el comando de pruebas |
| `CAMBIOS_README.md` | Este registro solicitado de lo cambiado, dónde y para qué |

## Cómo probarlo

1. Iniciar MySQL y ejecutar `python manage.py runserver` en el puerto 8000.
2. Abrir `/registro/` para crear una cuenta o `/login/` para usar una cuenta existente.
3. Entrar en Mantenimiento. Las tablas siguen usando Bootstrap Flatly, jQuery y DataTables.
4. Crear, editar o eliminar un tablero o una tarea. Las eliminaciones presentan confirmación antes de guardar el borrado.
5. Cerrar sesión y comprobar que mantenimiento vuelve a solicitar acceso.
6. Para recuperar una contraseña, usar el correo de una cuenta activa que tenga contraseña. Durante el desarrollo, buscar el enlace en la terminal del servidor.
7. Ejecutar `python manage.py test --settings=drf.test_settings` para las pruebas automáticas aisladas.

## Decisiones para mantener el alcance

- Se conserva el usuario nativo de Django y las cuentas existentes. La guía presenta `AbstractUser` y los campos personales adicionales como una posibilidad; no son necesarios para registrar e iniciar sesión. No se cambiaron modelos ni tablas ni se reinició la base.
- Se conserva el mantenimiento compartido del proyecto de clases: cualquier cuenta autenticada puede trabajar con esos registros. No se inventaron reglas de propiedad ni roles nuevos. Los usuarios y grupos se administran desde el administrador de Django, que ya estaba disponible.
- Se conservan las librerías visuales del profesor y los archivos estáticos locales.
- Se mantiene `DEBUG=True`, como la configuración actual del profesor, para trabajar con los estáticos en desarrollo. La plantilla 404 personalizada se conserva para `DEBUG=False`.
- El apartado de formato global de fechas es opcional. Se conserva el formato ISO de la API y la presentación de fechas en las tablas.
- Se mantiene el correo de desarrollo en consola mediante `MAILERS`, que corresponde a la versión de Django instalada. No se configuró un servicio externo ni se utilizaron credenciales de correo.
- Los tableros de demostración del navegador no se importan automáticamente a MySQL. Para trabajar con la base de datos se utiliza Mantenimiento.

## Verificación

- 14 pruebas automáticas sobre una base temporal: registro, contraseña cifrada, validación, login/logout, CSRF, acceso protegido, creación, edición, eliminación y recuperación/cambio de contraseña.
- Revisión de pantallas de acceso, registro y recuperación en el navegador. Comprobación de que la recuperación usa el diseño de TaskFlow y no el del administrador.
- Revisión independiente del código sin bloqueos importantes.
- No hay migraciones nuevas ni pendientes.
- Comprobación final completada: los usuarios, grupos, permisos y registros de tableros/tareas coinciden con el respaldo. Se conservan 3 usuarios, 6 tableros y 0 tareas. Todos los contadores automáticos coinciden con los valores anteriores y la próxima tarea mantiene el ID 1. No se crearon cuentas ni registros de prueba en MySQL.
- No se realizó commit ni push a GitHub.

## Respaldo previo

`C:/Users/rissx/Desktop/eva_backup_antes_completar_readme_2026-11-15_17-31-15`

Contiene el proyecto antes de estos cambios, el respaldo SQL y los valores de los contadores automáticos.
