from django.urls import path, include
from rest_framework import routers
from . import views


enrutador = routers.DefaultRouter()

enrutador.register(r'tableros', views.TableroViewSet)
enrutador.register(r'tareas', views.TareaViewSet)

urlpatterns = [
    path('', include(enrutador.urls)),
]
