from django.db import models

# Create your models here.
class users_temporal(models.Model):
    ROLES = (
        ('admin', 'Administrador'),
        ('mesero', 'mesero'),
        ('cajero', 'cajero'),
    )

    name = models.CharField(max_length=100, verbose_name="Nombre completo")
    email = models.EmailField(unique=True, verbose_name="Correo electrónico")
    pwd = models.TextField(verbose_name="Contraseña cifrada")
    rol = models.CharField(max_length=6, choices=ROLES, verbose_name="Rol de usuario")

    # Método String
    def __str__(self):
        return f"{self.name} ({self.rol}) - {self.email}"
