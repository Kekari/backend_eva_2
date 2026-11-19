from django.urls import path, include
from rest_framework import routers
from . import views


enrutador = routers.DefaultRouter()

enrutador.register(r'tableros', views.TableroViewSet, basename='tablero')
enrutador.register(r'tareas', views.TareaViewSet, basename='tarea')

urlpatterns = [
    path('', include(enrutador.urls)),
    path('grupo_tableros/listado_tableros', views.TableroListView.as_view(), name='listado_tableros'),
    path('grupo_tableros/crear_tablero', views.TableroCreateView.as_view(), name='crear_tablero'),
    path('grupo_tareas/listado_tareas', views.TareaListView.as_view(), name='listado_tareas'),
    path('grupo_tareas/crear_tarea', views.TareaCreateView.as_view(), name='crear_tarea'),
    path('grupo_tableros/editar_tablero/<int:pk>', views.TableroUpdateView.as_view(), name='editar_tablero'),
    path('grupo_tableros/eliminar_tablero/<int:pk>', views.TableroDeleteView.as_view(), name='eliminar_tablero'),
    path('grupo_tareas/editar_tarea/<int:pk>', views.TareaUpdateView.as_view(), name='editar_tarea'),
    path('grupo_tareas/eliminar_tarea/<int:pk>', views.TareaDeleteView.as_view(), name='eliminar_tarea'),
]
