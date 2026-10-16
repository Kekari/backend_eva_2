from django.shortcuts import render
from rest_framework import viewsets
from .models import Tablero, Tarea
from .serializer import TableroSerializer, TareaSerializer

# Create your views here.
def base(request):
    return render(request, 'inicio.html')


class TableroViewSet(viewsets.ModelViewSet):
    queryset = Tablero.objects.all()
    serializer_class = TableroSerializer


class TareaViewSet(viewsets.ModelViewSet):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer
