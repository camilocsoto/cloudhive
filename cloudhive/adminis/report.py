import pandas as pd
from django.utils.dateparse import parse_date
from io import BytesIO
from adminis.models import Sede
from cajero.models import Producto, DetallePedido

class SalesBySedeReport:
    """
    Igual que antes, pero ahora acepta un rango de fechas para filtrar
    pedidos completados (estado=1) por fecha_pedido.
    """

    def __init__(self, fecha_inicio=None, fecha_fin=None):
        """
        fecha_inicio, fecha_fin: strings 'YYYY-MM-DD' o date objects
        """
        # parsear strings a date si es necesario
        if isinstance(fecha_inicio, str):
            fecha_inicio = parse_date(fecha_inicio)
        if isinstance(fecha_fin, str):
            fecha_fin = parse_date(fecha_fin)

        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin

    def build_dataframe(self):
        # Base filter: pedidos completados
        filtros = {'pedido__estado': 1}

        # Añadir filtro de fecha si nos dieron ambas
        if self.fecha_inicio:
            filtros['pedido__fecha_pedido__date__gte'] = self.fecha_inicio
        if self.fecha_fin:
            filtros['pedido__fecha_pedido__date__lte'] = self.fecha_fin

        # Aplicar el filtro a los detalles
        detalles = DetallePedido.objects.filter(**filtros).select_related(
            'producto__sede'
        )

        rows = []
        for det in detalles:
            prod = det.producto
            sede = prod.sede
            if not sede:
                continue
            rows.append({
                'sede_id'         : sede.idSede,
                'sede_nombre'     : sede.nombre,
                'id_producto'     : prod.id,
                'nombre_producto' : prod.nombre,
                'cantidad'        : det.cantidad,
                'precio_compra'   : float(prod.precio_compra),
                'precio_venta'    : float(prod.precio_venta),
            })

        df = pd.DataFrame(rows)
        agg = df.groupby(
            ['sede_id','sede_nombre','id_producto','nombre_producto'],
            as_index=False
        ).agg({
            'cantidad':'sum',
            'precio_compra':'first',
            'precio_venta':'first'
        })

        agg['valor_compra'] = agg['precio_compra'] * agg['cantidad']
        agg['valor_venta']  = agg['precio_venta']  * agg['cantidad']
        agg['ganancia']     = agg['valor_venta']   - agg['valor_compra']

        return agg[[
            'id_producto',
            'nombre_producto',
            'cantidad',
            'valor_compra',
            'valor_venta',
            'ganancia',
            'sede_nombre'
        ]]

    def to_excel(self, df: pd.DataFrame) -> BytesIO:
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Reporte')
        output.seek(0)
        return output
