from django.urls import path
from . import views
from .views import *

app_name = 'cajero'

urlpatterns = [
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('nuevo/', views.crear_categoria, name='crear_categoria'),
    path('editar/<int:idCategoria>/', views.editar_categoria, name='editar_categoria'),
    path('eliminar/<int:idCategoria>/', views.eliminar_categoria, name='eliminar_categoria'),
    # productos
    path('productos/', ProductoListView.as_view(), name='producto_list'),
    path('productos/crear/', ProductoCreateView.as_view(), name='producto_create'),
    path('productos/<int:pk>/editar/', ProductoUpdateView.as_view(), name='producto_update'),
    path('productos/<int:pk>/eliminar/', ProductoDeleteView.as_view(), name='producto_delete'),  
    # ver mesas de la sede
    path('', views.MesaListByUserView.as_view(), name='user_mesas'),
    path('detalle/<int:pk>', views.MesaDetailView.as_view(), name='detalle_mesa'),
    # ver pedidos de la sede
    path('pedidos/', PedidoListView.as_view(), name='pedido_list'),
    
    path('reporte/', ReporteFormView.as_view(), name='reporte_form'),
]
