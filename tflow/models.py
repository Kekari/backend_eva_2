from django.conf import settings
from django.db import models


class Tablero(models.Model):
    COLORES = [
        ('purple', 'Lila'),
        ('green', 'Salvia'),
        ('peach', 'Durazno'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tableros',
    )
    titulo = models.CharField('Título', max_length=60)
    descripcion = models.TextField('Descripción', max_length=160, blank=True)
    color = models.CharField('Color', max_length=10, choices=COLORES, default='purple')
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Fecha de actualización', auto_now=True)

    def __str__(self):
        return self.titulo


class Tarea(models.Model):
    ESTADOS = [
        (0, 'Pendiente'),
        (1, 'En progreso'),
        (2, 'Completado'),
    ]

    tablero = models.ForeignKey(
        Tablero,
        on_delete=models.CASCADE,
        related_name='tareas',
    )
    titulo = models.CharField('Título', max_length=140)
    descripcion = models.TextField('Descripción', blank=True)
    estado = models.IntegerField('Estado', choices=ESTADOS, default=0)
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Fecha de actualización', auto_now=True)

    def __str__(self):
        return self.titulo
