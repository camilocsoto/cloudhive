from django.urls import path
from .views import *

urlpatterns = [
    path('', lista_mesas, name = "mesas"),
    path('verpedidos/', ver_pedidos, name='ver_pedidos'),
    path("cancelar-mesa/", cancelar_mesa, name="cancelar_mesa"),
    path('agregar-producto/', agregar_producto_pedido, name='agregar_producto'),

]
