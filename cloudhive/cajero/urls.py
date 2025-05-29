from django.urls import path
from . import views

app_name = 'cajero'

urlpatterns = [
    path('', views.lista_categorias, name='lista_categorias'),
    path('nuevo/', views.crear_categoria, name='crear_categoria'),
    path('editar/<int:idCategoria>/', views.editar_categoria, name='editar_categoria'),
    path('eliminar/<int:idCategoria>/', views.eliminar_categoria, name='eliminar_categoria'),
    path('productos/', views.lista_productos, name='productos'),
    path('productos/crear_producto', views.lista_productos, name='crear_productos'),
    
]
