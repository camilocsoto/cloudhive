from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario

# Formulario para la creación de usuarios (usado en el admin)
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        # Incluye los campos que deseas que se ingresen al crear un usuario.
        # Nota: 'username' se maneja automáticamente en el método save() de tu modelo.
        fields = ('correo', 'nombres', 'apellidos', 'tipoDocumento', 'numDocumento', 'rol', 'estado')

# Formulario para editar usuarios (usado en el admin)
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields = ('correo', 'nombres', 'apellidos', 'tipoDocumento', 'numDocumento', 'rol', 'estado')

# Configuración del administrador personalizado para el modelo Usuario.
class UsuarioAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Usuario
    list_display = ('correo', 'nombres', 'apellidos', 'tipoDocumento', 'numDocumento', 'rol', 'estado', 'is_staff', 'sede')
    list_filter = ('rol', 'estado', 'is_staff')
    
    # Configuración de los campos al editar un usuario.
    fieldsets = (
        (None, {'fields': ('username', 'correo', 'password')}),
        ('Información Personal', {'fields': ('nombres', 'apellidos', 'tipoDocumento', 'numDocumento')}),
        ('Permisos', {'fields': ('rol', 'estado', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Configuración de los campos al crear un usuario.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'correo', 'nombres', 'apellidos', 'tipoDocumento', 'numDocumento', 'rol', 'estado', 'password1', 'password2','sede'),
        }),
    )
    
    search_fields = ('correo', 'nombres', 'apellidos', 'numDocumento')
    ordering = ('correo',)
    
# Se registra el modelo Usuario en el admin usando la configuración personalizada.
admin.site.register(Usuario, UsuarioAdmin)
