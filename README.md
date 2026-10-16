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
