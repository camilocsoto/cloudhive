from django.shortcuts import render, redirect, get_object_or_404
from .models import Categoria
from .forms.categoria_form import CategoriaForm

def lista_categorias(request):
    categorias = Categoria.objects.all() 
    print(categorias) 
    return render(request, 'lista.html', {'categorias': categorias})


def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)  
        if form.is_valid():
            form.save()  # Guardar la nueva categoría
            return redirect('lista_categorias') 
    else:
        form = CategoriaForm()  # Crear un formulario vacío para el método GET
    return render(request, 'formulario.html', {'form': form})  

def editar_categoria(request, idCategoria):
    categoria = get_object_or_404(Categoria, idCategoria=idCategoria)  # Obtener la categoría por id
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)  # Rellenar el formulario con los datos de la categoría
        if form.is_valid():
            form.save() 
            return redirect('lista_categorias') 
    else:
        form = CategoriaForm(instance=categoria)  # Crear el formulario con los datos de la categoría a editar
    return render(request, 'formulario.html', {'form': form})  

def eliminar_categoria(request, idCategoria):
    categoria = get_object_or_404(Categoria, idCategoria=idCategoria)  
    if request.method == 'POST':
        categoria.delete()  # Eliminar la categoría
        return redirect('lista_categorias')  
    return render(request, 'confirmar_eliminar.html', {'categoria': categoria}) 
