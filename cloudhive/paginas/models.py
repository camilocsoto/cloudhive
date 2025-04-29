from django.db import models

# Create your models here.
class Categoria2(models.Model):
    idCategoria = models.AutoField(primary_key=True)  
    nombre = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre  
    
class Proveedor(models.Model):
    idProveeedor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)
     
    def __str__(self):
        return self.nombre

class Ciudad(models.Model):
    idCiudad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)
     
    def __str__(self):
        return self.nombre
    
class MetodoPago(models.Model):
    idMetodoPago = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre
    
class Sede(models.Model):
    idMesa = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)
    idCiudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre
    
class Usuario2(models.Model):
    idUsuario = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    tipoDocumento = models.CharField(max_length=5)
    numDocumento = models.CharField(max_length=20)
    correo = models.CharField(max_length=150)
    password = models.CharField(max_length=100)
    rol = models.IntegerField()
    estado= models.IntegerField(verbose_name="Estado")
    idSede = models.ForeignKey(Sede, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombres
    
class Producto(models.Model):
    idProducto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    stock = models.IntegerField()
    precioCompra = models.FloatField()
    precioVenta = models.FloatField()
    idSede = models.ForeignKey(Sede, on_delete=models.CASCADE)
    idCategoria = models.ForeignKey(Categoria2, on_delete=models.CASCADE)
    idProveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre
    
class Mesa(models.Model):
    idMesa = models.AutoField(primary_key=True)
    numeroMesa = models.CharField(max_length=100)
    Disponibilidad = models.IntegerField()
    idSede = models.ForeignKey(Sede, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.numeroMesa

class Pedido(models.Model):
    idPedido = models.AutoField(primary_key=True)
    estado = models.IntegerField()
    fhaPedido = models.DateTimeField()
    totalPago = models.FloatField()
    idMetodoPago = models.ForeignKey(MetodoPago, on_delete=models.CASCADE)
    idMesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.idPedido

class detallePedido(models.Model):
    idProducto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    idMesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.idProducto