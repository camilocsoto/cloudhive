from django.urls import reverse_lazy

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Sede, Pais, Ciudad
from accounts.models import Usuario
from .forms import SedeForm, PaisForm, CiudadForm, UsuarioForm
from django.contrib.auth.mixins import LoginRequiredMixin

class SedeListView(LoginRequiredMixin, ListView):
    model = Sede
    template_name = 'sedes/sede_list.html'
    context_object_name = 'sedes'

class SedeCreateView(CreateView):
    model = Sede
    form_class = SedeForm
    template_name = 'sedes/sede_form.html'
    success_url = reverse_lazy('adminis:list_sede')

class SedeUpdateView(UpdateView):
    model = Sede
    form_class = SedeForm
    template_name = 'sedes/sede_form.html'
    success_url = reverse_lazy('adminis:list_sede')

class SedeDeleteView(DeleteView):
    model = Sede
    template_name = 'sedes/sede_confirm_delete.html'
    success_url = reverse_lazy('adminis:list_sede')

# Vistas para paises

class PaisListView(LoginRequiredMixin, ListView):
    model = Pais
    template_name = 'pais/pais_list.html'
    context_object_name = 'paises'

class PaisCreateView(LoginRequiredMixin, CreateView):
    model = Pais
    form_class = PaisForm
    template_name = 'pais/pais_form.html'
    success_url = reverse_lazy('adminis:list_pais')

class PaisUpdateView(LoginRequiredMixin, UpdateView):
    model = Pais
    form_class = PaisForm
    template_name = 'pais/pais_form.html'
    success_url = reverse_lazy('adminis:list_pais')

class PaisDeleteView(LoginRequiredMixin, DeleteView):
    model = Pais
    template_name = 'pais/pais_confirm_delete.html'
    success_url = reverse_lazy('adminis:list_pais')
    
# Vistas para ciudades

class CiudadListView(LoginRequiredMixin, ListView):
    model = Ciudad
    template_name = 'ciudad/ciudad_list.html'
    context_object_name = 'ciudades'

class CiudadCreateView(LoginRequiredMixin, CreateView):
    model = Ciudad
    form_class = CiudadForm
    template_name = 'ciudad/ciudad_form.html'
    success_url = reverse_lazy('adminis:list_ciudad')

class CiudadUpdateView(LoginRequiredMixin, UpdateView):
    model = Ciudad
    form_class = CiudadForm
    template_name = 'ciudad/ciudad_form.html'
    success_url = reverse_lazy('adminis:list_ciudad')

class CiudadDeleteView(LoginRequiredMixin, DeleteView):
    model = Ciudad
    template_name = 'ciudad/ciudad_confirm_delete.html'
    success_url = reverse_lazy('adminis:list_ciudad')
    
    # vistas para usuarios
    
class UsuarioListView(LoginRequiredMixin, ListView):
    model = Usuario
    template_name = 'usuario/usuario_list.html'
    context_object_name = 'usuarios'

class UsuarioCreateView(LoginRequiredMixin, CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'usuario/usuario_form.html'
    success_url = reverse_lazy('adminis:list_usuario')

class UsuarioUpdateView(LoginRequiredMixin, UpdateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'usuario/usuario_form.html'
    success_url = reverse_lazy('adminis:list_usuario')

class UsuarioDeleteView(LoginRequiredMixin, DeleteView):
    model = Usuario
    template_name = 'usuario/usuario_confirm_delete.html'
    success_url = reverse_lazy('adminis:list_usuario')