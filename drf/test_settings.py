from .settings import *

# Pruebas aisladas: no crean registros ni consumen IDs en MySQL.
DATABASES = {
    'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'},
}
