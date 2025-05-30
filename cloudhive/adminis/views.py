from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View, TemplateView
from .models import Sede, Pais, Ciudad
from accounts.models import Usuario
from mesero.models import Mesa
from .forms import SedeForm, PaisForm, CiudadForm, UsuarioForm, MesaForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from .report import SalesBySedeReport
from datetime import date

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
    
    # cambio de rol de admin.
    
class ChangeRolView(LoginRequiredMixin, DetailView):
    # Acceso al html de cambio de rol
    model = Sede
    template_name = 'sedes/cambiar_rol.html'
    context_object_name = 'sede'
    def get_context_data(self, **kwargs):
        # carga info del usuario.
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user 
        # carga info de las mesas del foreign key.
        context['mesas'] = self.object.mesas.all()
        return context

class UpdateUserRoleView(LoginRequiredMixin, View):
    # cambia id de sede del usuario y redirecciona a la vista correspondiente.
    def post(self, request, pk):
        new_role = request.POST.get('new_role')
        new_sede = get_object_or_404(Sede, pk=pk) # asign id sede to the user
        user = request.user
        user.sede = new_sede
        user.save()
        # Cambia la url del administrador según el rol elegido.
        if new_role == '2':
            return redirect('cajero:user_mesas')
        if new_role == '3':
            # cambiar a la vista del mesero 🛠️
            return redirect('adminis:list_sede')
        return redirect('adminis:list_sede')    
    
    # vistas de mesas.

class MesaCreateView(LoginRequiredMixin, CreateView):
    model = Mesa
    form_class = MesaForm
    template_name = 'mesas/mesa_form.html'

    def form_valid(self, form):
        form.instance.sede = get_object_or_404(Sede, pk=self.kwargs['sede_pk'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sede'] = get_object_or_404(Sede, pk=self.kwargs['sede_pk'])
        return context

    def get_success_url(self):
        return reverse_lazy('adminis:change_rol', kwargs={'pk': self.kwargs['sede_pk']})

class MesaUpdateView(LoginRequiredMixin, UpdateView):
    model = Mesa
    form_class = MesaForm
    template_name = 'mesas/mesa_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Esto pone en plantilla la sede a la que pertenece la mesa actual
        context['sede'] = self.object.sede
        return context

    def get_success_url(self):
        return reverse_lazy('adminis:change_rol', kwargs={'pk': self.object.sede.pk})
    
class MesaDeleteView(LoginRequiredMixin, DeleteView):
    model = Mesa
    template_name = 'mesas/mesa_confirm_delete.html'

    def get_success_url(self):
        # regresa al menú anterior
        return reverse_lazy('adminis:change_rol', kwargs={'pk': self.object.sede.pk})
    
# Reporte de ventas por sede
class SalesBySedeExcelView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        fi = request.GET.get('fecha_inicio')
        ff = request.GET.get('fecha_fin')
        # si el rol NO es admin (1), filtramos por su sede
        sede_id = None
        if request.user.rol != 1:
            sede_id = request.user.sede_id

        report = SalesBySedeReport(fecha_inicio=fi, fecha_fin=ff, sede_id=sede_id)
        df     = report.build_dataframe()
        excel  = report.to_excel(df)

        filename = "sales_report"
        if fi and ff:
            filename += f"_{fi}_to_{ff}"
        filename += ".xlsx"

        resp = HttpResponse(
            excel.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        resp['Content-Disposition'] = f'attachment; filename=\"{filename}\"'
        return resp
    
    def get_context_data(self, **kwargs):
        # para renderizar el form si es plantilla; si no la usas déjalo así
        context = super().get_context_data(**kwargs)
        context['today'] = date.today().isoformat()
        return context



class ReporteFormView(LoginRequiredMixin, TemplateView):
    template_name = 'report/report_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = date.today().isoformat()  # 'YYYY-MM-DD'
        return context