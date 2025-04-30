from django.db import models

class Pais(models.Model):
    ESTADO = (
        (0, 'inactivo'),
        (1, 'activo')
    )
    idPais = models.AutoField(primary_key=True, db_column='idPais')
    Nombre = models.CharField(max_length=45, null=True, db_column='Nombre')
    estado = models.IntegerField(choices=ESTADO, null=True, default=1,db_column='estado')

    class Meta:
        db_table = 'Pais'
        managed = True
        verbose_name = 'País'
        verbose_name_plural = 'Países'

    def __str__(self):
        return self.Nombre or f'País {self.idPais}'


class Ciudad(models.Model):
    ESTADO = (
        (0, 'inactivo'),
        (1, 'activo')
    )
    idCiudad = models.AutoField(primary_key=True, db_column='idCiudad')
    nombre = models.CharField(max_length=45, null=True, db_column='nombre')
    estado = models.IntegerField(choices=ESTADO, null=True, default=1,db_column='estado')
    Pais = models.ForeignKey(
        Pais,
        on_delete=models.PROTECT,
        db_column='Pais_idPais',
        related_name='ciudades',
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'Ciudad'
        managed = True
        verbose_name = 'Ciudad'
        verbose_name_plural = 'Ciudades'

    def __str__(self):
        return self.nombre or f'Ciudad {self.idCiudad}'


class Sede(models.Model):
    
    ESTADO = (
        (0, 'inactivo'),
        (1, 'activo')
    )
    
    idSede = models.AutoField(primary_key=True, db_column='idSede')
    nombre = models.CharField(max_length=100, null=True, db_column='nombre')
    estado = models.IntegerField(choices=ESTADO, null=True, default=1,db_column='estado')
    Ciudad = models.ForeignKey(
        Ciudad,
        on_delete=models.PROTECT,
        db_column='Ciudad_idCiudad',
        related_name='sedes',
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'Sede'
        managed = True
        verbose_name = 'Sede'
        verbose_name_plural = 'Sedes'

    def __str__(self):
        return self.nombre or f'Sede {self.idSede}'
