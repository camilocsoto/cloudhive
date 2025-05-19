from django.db import models
from django.contrib.auth.models import AbstractUser
from adminis.models import Sede

class Usuario(AbstractUser):
    
    TYPEDOCS = (
        ('cc', 'cédula de ciudadania'),
        ('ti', 'tarjeta de identidad'),
        ('ce', 'cédula de extranjería'),
        ('pa', 'pasaporte'),
    )
    ROLES = (
        (1, 'Admin'),
        (2, 'cajero'),
        (3, 'mesero'),
    )
    ESTADO = (
        (0, 'inactivo'),
        (1, 'activo')
    )
    # idUsuario -> Django crea lo automáticamente
    nombres = models.CharField(max_length=100, verbose_name='Nombre(s)')
    apellidos = models.CharField(max_length=100, verbose_name='Apellido(s)')
    tipoDocumento = models.CharField(max_length=5, choices=TYPEDOCS, verbose_name='Tipo de documento')
    numDocumento = models.CharField(max_length=20, unique=True, verbose_name='Número de documento')
    correo = models.EmailField(max_length=100, unique=True, verbose_name='Correo electrónico')
    # 'password' ya existe en AbstractUser
    rol = models.IntegerField(choices=ROLES, default=3)
    estado = models.BooleanField(choices=ESTADO, default=0)
    # Nueva relación opcional a Sede
    sede = models.ForeignKey(
        Sede,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios',
        verbose_name='Sede asignada'
    )

    # Django por defecto en AbstractUser ya tiene campos: username, password, first_name, last_name, email, is_staff, is_active, is_superuser, etc.
    # para usar en la creación de superusuarios
    REQUIRED_FIELDS = ['nombres', 'apellidos', 'tipoDocumento', 'numDocumento', 'rol', 'estado', 'correo']

    def save(self, *args, **kwargs):
        # Si no se define username manualmente, se asigna el valor de correo.
        if not self.username and self.correo:
            self.username = self.correo
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.correo}"
