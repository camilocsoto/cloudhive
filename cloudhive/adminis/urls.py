from django.urls import path
from .views import *

app_name = 'adminis'

urlpatterns = [
    path('', SedeListView.as_view(), name='list_sede'),
    path('crear/', SedeCreateView.as_view(), name='create_sede'),
    path('<int:pk>/editar/', SedeUpdateView.as_view(), name='update_sede'),
    path('<int:pk>/eliminar/', SedeDeleteView.as_view(), name='delete_sede'),
    # --- Países ---
    path('pais/', PaisListView.as_view(), name='list_pais'),
    path('pais/crear/', PaisCreateView.as_view(), name='create_pais'),
    path('pais/<int:pk>/editar/', PaisUpdateView.as_view(), name='update_pais'),
    path('pais/<int:pk>/eliminar/',PaisDeleteView.as_view(), name='delete_pais'),
    # --- Ciudades ---
    path('ciudad/', CiudadListView.as_view(), name='list_ciudad'),
    path('ciudad/crear/', CiudadCreateView.as_view(), name='create_ciudad'),
    path('ciudad/<int:pk>/editar/', CiudadUpdateView.as_view(), name='update_ciudad'),
    path('ciudad/<int:pk>/eliminar/', CiudadDeleteView.as_view(), name='delete_ciudad'),
    # --- Usuarios ---
    path('usuario/', UsuarioListView.as_view(), name='list_usuario'),
    path('usuario/crear/', UsuarioCreateView.as_view(), name='create_usuario'),
    path('usuario/<int:pk>/editar/', UsuarioUpdateView.as_view(), name='update_usuario'),
    path('usuario/<int:pk>/eliminar/', UsuarioDeleteView.as_view(), name='delete_usuario'),
    # -- cambiar rol --
    path('sede/<int:pk>/detalles/', ChangeRolView.as_view(), name='change_rol'),
    path('sede/<int:pk>/update-rol/', UpdateUserRoleView.as_view(), name='update_user_rol'),
    # -- mesas --
    path('sede/<int:sede_pk>/mesas/crear/', MesaCreateView.as_view(), name='create_mesa'),
    path( 'mesas/<int:pk>/editar/', MesaUpdateView.as_view(), name='update_mesa'),
    path( 'mesas/<int:pk>/eliminar/', MesaDeleteView.as_view(), name='delete_mesa'),
    
]
    