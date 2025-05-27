from django.db import models
from adminis.models import Sede
from mesero.models import Mesa

class Categoria(models.Model):
    idCategoria = models.AutoField(primary_key=True)  
    nombre = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre  


class MetodoPago(models.Model):
    
    ESTADO = (
    (0, 'disponible'),
    (1, 'ocupado')
    )
    # 'idMetodo' -> Django lo crea automáticamente
    nombre = models.CharField(max_length=45, verbose_name='Nombre del método de pago')    
    estado = models.BooleanField(choices=ESTADO, default=0, verbose_name='Estado de la mesa')
    
    def __str__(self):
        return f'método de pago {self.nombre} está {"disponible" if self.estado == 0 else "ocupado"}'

class Proveedor(models.Model):
    ESTADO = (
    (0, 'inactivo'),
    (1, 'activo')
    )
    # 'idProv' -> Django lo crea automáticamente
    nombre = models.CharField(max_length=100, verbose_name='Nombre del proveedor')
    estado = models.BooleanField(choices=ESTADO, default=1, verbose_name='Estado del proveedor')
        
    def __str__(self):
        return f'proveedor {self.nombre} está {"activo" if self.estado == 1 else "inactivo"}'
    
    
class Producto(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre del producto')
    stock = models.PositiveIntegerField(default=0, verbose_name='Cantidad en stock')
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio de compra del producto')
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio de venta del producto')
    sede = models.ForeignKey(
        Sede, on_delete=models.CASCADE, null=True, blank=True, related_name='producto_sede', verbose_name='Sede asignada'
    )
    categoria = models.ForeignKey(
        Categoria, on_delete=models.CASCADE, null=True, blank=True, related_name='producto_categoria', verbose_name='Categoría'
    )
    proveedor = models.ForeignKey(
        Proveedor, on_delete=models.CASCADE, null=True, blank=True, related_name='producto_proveedor', verbose_name='Proveedor'
    )
    def __str__(self):
        return f'producto {self.nombre} tiene {self.stock} en la sede {self.sede.nombre if self.sede else "sin sede"}'
    

class Pedido(models.Model):
    ESTADO = (
        (0, 'pendiente'),
        (1, 'completado'),
    )
    estado = models.BooleanField(choices=ESTADO, default=0, verbose_name='Estado del pedido')
    fecha_pedido = models.DateTimeField(auto_now_add=True, verbose_name='Fecha del pedido')
    pago_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Pago total del pedido')    
    metodo_pago = models.ForeignKey(
        MetodoPago, on_delete=models.DO_NOTHING, related_name='pedido_metodo', verbose_name='Método de pago'
    )    
    mesa = models.ForeignKey(
        Mesa, on_delete=models.DO_NOTHING, related_name='pedido_mesa', verbose_name='Mesa asignada'
    )
    # Relación M2M usando el modelo intermedio DetallePedido
    productos = models.ManyToManyField(
        Producto, through='DetallePedido', related_name='pedidos', verbose_name='Productos del pedido'
    )

    def __str__(self):
        return f'pedido {self.id} del proveedor {self.proveedor.nombre} está {"pendiente" if self.estado == 0 else "completado" if self.estado == 1 else "cancelado"}'
    
class DetallePedido(models.Model):    
    # Modelo intermedio que une Pedido y Producto
    
    cantidad = models.PositiveIntegerField( default=1, verbose_name='Cantidad')
    
    pedido   = models.ForeignKey(
        Pedido, on_delete=models.CASCADE, related_name='lineas_producto', verbose_name='Pedido'
    )
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, related_name='lineas_pedido', verbose_name='Producto'
    )
    class Meta:
        unique_together = ('pedido', 'producto')
        verbose_name = 'Línea de pedido'
        verbose_name_plural = 'Líneas de pedido'

    def __str__(self):
        return f'{self.cantidad}× {self.producto.nombre} en Pedido #{self.pedido.id}'    