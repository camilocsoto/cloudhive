from django.shortcuts import render, redirect, get_object_or_404
from .models import Categoria, Producto
from .forms.categoria_form import CategoriaForm
# home/views.py
from django.views.generic import TemplateView

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

# Vista para root
# home/views.py

class HomeView(TemplateView):
    template_name = "inicio.html"

# Productos
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'producto/productos.html', {'productos': productos})
