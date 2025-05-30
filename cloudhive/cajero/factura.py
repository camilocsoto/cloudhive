import pandas as pd
from django.db.models import F
from cajero.models import DetallePedido


def generar_factura_por_mesa(mesa_id):
    """
    Genera un DataFrame con los detalles del pedido vigente (estado=True) para una mesa dada,
    calcula subtotal y total, y devuelve el DataFrame, total y fecha del pedido.
    Si no hay pedido vigente, retorna DataFrame vacío y total 0.
    """
    # Filtrar detalle de pedido para el pedido vigente (estado=True) de la mesa, tomando el más reciente
    detalles = (
        DetallePedido.objects
        .filter(pedido__mesa_id=mesa_id, pedido__estado=True)
        .select_related('producto', 'pedido')
        .order_by('-pedido__id')
    )
    
    data = []
    fecha_pedido = None
    if detalles:
        # Agrupar por producto dentro del último pedido activo
        ultimo_pedido = detalles[0].pedido
        fecha_pedido = ultimo_pedido.fecha_pedido
        # Construir registros únicos por detalle (ya viene unique por pedido-producto)
        for detalle in detalles:
            prod = detalle.producto
            subtotal = detalle.cantidad * prod.precio_venta
            data.append({
                'producto': prod.nombre,
                'cantidad': detalle.cantidad,
                'precio_unitario': float(prod.precio_venta),
                'subtotal': float(subtotal)
            })
    # Crear DataFrame
    df = pd.DataFrame(data)
    # Calcular total
    total = df['subtotal'].sum() if not df.empty else 0.0

    return df, total, fecha_pedido
