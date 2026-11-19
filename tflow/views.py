from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from .models import Tablero, Tarea
from .serializer import TableroSerializer, TareaSerializer
from .forms import TableroForm, TareaForm, RegistroForm

# Create your views here.
@never_cache
def base(request):
    bienvenida = request.session.pop('mensaje_bienvenida', None)
    if bienvenida:
        messages.success(request, bienvenida)
    return render(request, 'inicio.html')


@never_cache
@require_http_methods(['GET', 'POST'])
def registro(request):
    if request.user.is_authenticated:
        return redirect('base')
    form = RegistroForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        usuario = form.save()
        login(request, usuario)
        request.session['mensaje_bienvenida'] = f'¡Bienvenido, {usuario.username}! Tu cuenta está lista.'
        return redirect('base')
    return render(request, 'registration/registro.html', {'form': form})


class TableroViewSet(viewsets.ModelViewSet):
    serializer_class = TableroSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Tablero.objects.filter(usuario=self.request.user).order_by('pk')

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class TareaViewSet(viewsets.ModelViewSet):
    serializer_class = TareaSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Tarea.objects.filter(tablero__usuario=self.request.user).order_by('pk')

    def perform_create(self, serializer):
        tablero = serializer.validated_data['tablero']
        if tablero.usuario_id != self.request.user.id:
            raise PermissionDenied('Ese tablero no pertenece a tu cuenta.')
        serializer.save()

    def perform_update(self, serializer):
        tablero = serializer.validated_data.get('tablero', serializer.instance.tablero)
        if tablero.usuario_id != self.request.user.id:
            raise PermissionDenied('Ese tablero no pertenece a tu cuenta.')
        serializer.save()


class TableroListView(LoginRequiredMixin, ListView):
    model = Tablero
    queryset = Tablero.objects.select_related('usuario').order_by('pk')
    template_name = 'tflow/tablero/listado_tableros.html'


class TableroCreateView(LoginRequiredMixin, CreateView):
    model = Tablero
    form_class = TableroForm
    template_name = 'tflow/tablero/crear_tablero.html'
    success_url = reverse_lazy('listado_tableros')


class TareaListView(LoginRequiredMixin, ListView):
    model = Tarea
    queryset = Tarea.objects.select_related('tablero').order_by('pk')
    template_name = 'tflow/tarea/listado_tareas.html'


class TareaCreateView(LoginRequiredMixin, CreateView):
    model = Tarea
    form_class = TareaForm
    template_name = 'tflow/tarea/crear_tarea.html'
    success_url = reverse_lazy('listado_tareas')


class TableroUpdateView(LoginRequiredMixin, UpdateView):
    model = Tablero
    form_class = TableroForm
    template_name = 'tflow/tablero/editar_tablero.html'
    success_url = reverse_lazy('listado_tableros')


class TareaUpdateView(LoginRequiredMixin, UpdateView):
    model = Tarea
    form_class = TareaForm
    template_name = 'tflow/tarea/editar_tarea.html'
    success_url = reverse_lazy('listado_tareas')


class TableroDeleteView(LoginRequiredMixin, DeleteView):
    model = Tablero
    template_name = 'tflow/tablero/eliminar_tablero.html'
    success_url = reverse_lazy('listado_tableros')
    http_method_names = ['get', 'post', 'head', 'options']


class TareaDeleteView(LoginRequiredMixin, DeleteView):
    model = Tarea
    template_name = 'tflow/tarea/eliminar_tarea.html'
    success_url = reverse_lazy('listado_tareas')
    http_method_names = ['get', 'post', 'head', 'options']
