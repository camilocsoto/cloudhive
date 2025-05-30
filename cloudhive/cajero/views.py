from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Categoria, Producto, Pedido, DetallePedido
from mesero.models import Mesa
from .forms.categoria_form import CategoriaForm
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from .factura import generar_factura_por_mesa
from .forms.pago_form import ConfirmarPagoForm
from .forms.producto_form import ProductoForm
from decimal import Decimal
from datetime import date

# Vista para root
class HomeView(TemplateView):
    template_name = "inicio.html"

# CRUD de categorias
def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'categoria/lista.html', {'categorias': categorias})

def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cajero:lista_categorias')    # <- aquí
    else:
        form = CategoriaForm()
    return render(request, 'categoria/formulario.html', {'form': form})

def editar_categoria(request, idCategoria):
    categoria = get_object_or_404(Categoria, idCategoria=idCategoria)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('cajero:lista_categorias')    # <- y aquí
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'categoria/formulario.html', {'form': form})

def eliminar_categoria(request, idCategoria):
    categoria = get_object_or_404(Categoria, idCategoria=idCategoria)
    if request.method == 'POST':
        categoria.delete()
        return redirect('cajero:lista_categorias')    # <- y aquí
    return render(request, 'categoria/confirmar_eliminar.html', {'categoria': categoria})


# CRUD Productos
class ProductoListView(LoginRequiredMixin, ListView):
    model = Producto
    template_name = 'producto/producto_list.html'
    context_object_name = 'productos'

    def get_queryset(self):
        # Mostrar solo los productos de la sede del usuario
        user_sede = self.request.user.sede
        return Producto.objects.filter(sede=user_sede)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['usuario'] = self.request.user
        ctx['sede']    = self.request.user.sede
        return ctx

class ProductoCreateView(LoginRequiredMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'producto/producto_form.html'

    def form_valid(self, form):
        # Asignar la sede del usuario al producto
        form.instance.sede = self.request.user.sede
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('cajero:producto_list')

class ProductoUpdateView(LoginRequiredMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'producto/producto_form.html'

    def get_success_url(self):
        return reverse_lazy('cajero:producto_list')

class ProductoDeleteView(LoginRequiredMixin, DeleteView):
    model = Producto
    template_name = 'producto/producto_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('cajero:producto_list')


# R de pedidos
class PedidoListView(LoginRequiredMixin, ListView):
    model = Pedido
    template_name = 'factura/pedido_list.html'
    context_object_name = 'pedidos'

    def get_queryset(self):
        user_sede = self.request.user.sede
        # Mostrar solo pedidos cuya mesa pertenece a la sede del usuario
        return Pedido.objects.filter(mesa__sede=user_sede).order_by('-fecha_pedido')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['sede']    = self.request.user.sede
        ctx['usuario'] = self.request.user
        return ctx
    

# factura: nivel de dificultad y comprensión: hard
class MesaListByUserView(LoginRequiredMixin, ListView):
    # lista de todas las mesas de la sede
    model = Mesa
    template_name = 'factura/mesa_list_by_user.html'
    context_object_name = 'mesas'

    def get_queryset(self):
        # Solo las mesas cuya sede coincide con la del usuario en sesión
        user_sede = self.request.user.sede
        return Mesa.objects.filter(sede=user_sede)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['usuario'] = self.request.user
        ctx['sede']    = self.request.user.sede
        return ctx
    
class MesaDetailView(LoginRequiredMixin, FormMixin, DetailView):
    # Detalle de una mesa con su factura y cancela el pago
    model = Mesa
    template_name = 'factura/mesa_detail.html'
    context_object_name = 'mesa'
    form_class = ConfirmarPagoForm
    success_url = reverse_lazy('cajero:user_mesas')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # factura
        df, total, fecha = generar_factura_por_mesa(self.object.pk)
        ctx['factura_records'] = df.to_dict('records')
        ctx['total_factura']   = total
        ctx['fecha_pedido']    = fecha
        # Formulario
        ctx['form'] = self.get_form()
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()   # necesario para DetailView
        form = self.get_form()
        if form.is_valid():
            # Pedido vigente
            pedido = Pedido.objects.filter(mesa=self.object, estado=True).last()
            if pedido:
                # 1) Actualizar método de pago y estado del pedido
                pedido.metodo_pago = form.cleaned_data['metodo_pago']
                pedido.pago_total    = Decimal(self.get_context_data()['total_factura']).quantize(Decimal('0.01'))
                pedido.estado        = False   # ya completado
                pedido.save()

                # 2) Ajustar stock de cada producto en el detalle
                for detalle in DetallePedido.objects.filter(pedido=pedido):
                    prod = detalle.producto
                    prod.stock = prod.stock - detalle.cantidad
                    prod.save()

                # 3) Liberar la mesa
                self.object.estado = False
                self.object.save()

            return redirect(self.get_success_url())

        # si no es válido, volver a renderizar con errores
        return self.render_to_response(self.get_context_data(form=form))
    
    
# reporte de ventas por sede
class ReporteFormView(LoginRequiredMixin, TemplateView):
    template_name = 'report/report.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = date.today().isoformat()  # 'YYYY-MM-DD'
        return context