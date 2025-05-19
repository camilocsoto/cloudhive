from django.db import models
from adminis.models import Sede

ESTADO = (
    (0, 'disponible'),
    (1, 'ocupado')
)

# Create your models here.
class Mesa(models.Model):
    # 'idMesa' -> Django lo crea automáticamente
    nombre = models.CharField(max_length=100, verbose_name='Nombre de la mesa')
    capacidad = models.IntegerField(max_length=30, verbose_name='Capacidad de la mesa')
    estado = models.BooleanField(choices=ESTADO, default=0, verbose_name='Estado de la mesa')
    sede = models.ForeignKey(
        Sede,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='mesas',
        verbose_name='Sede asignada'
    )
    
    
    def __str__(self):
        return f'mesa {self.nombre} de cap. {self.capacidad} de la sede {self.sede.nombre}'