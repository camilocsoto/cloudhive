from django.db import models

class Categoria(models.Model):
    idCategoria = models.AutoField(primary_key=True)  
    nombre = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre  