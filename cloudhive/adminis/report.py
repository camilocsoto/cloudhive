import pandas as pd
from django.utils.dateparse import parse_date
from io import BytesIO
from cajero.models import DetallePedido

class SalesBySedeReport:
    """
    Ahora acepta un parámetro opcional `sede_id` para filtrar.
    """

    def __init__(self, fecha_inicio=None, fecha_fin=None, sede_id=None):
        # parseo de fechas como antes...
        if isinstance(fecha_inicio, str):
            fecha_inicio = parse_date(fecha_inicio)
        if isinstance(fecha_fin, str):
            fecha_fin = parse_date(fecha_fin)

        self.fecha_inicio = fecha_inicio
        self.fecha_fin    = fecha_fin
        self.sede_id      = sede_id

    def build_dataframe(self):
        filtros = {'pedido__estado': 1}

        if self.fecha_inicio:
            filtros['pedido__fecha_pedido__date__gte'] = self.fecha_inicio
        if self.fecha_fin:
            filtros['pedido__fecha_pedido__date__lte'] = self.fecha_fin
        if self.sede_id is not None:
            # solo pedimos detalles cuyo pedido pertenece a mesa en esta sede
            filtros['pedido__mesa__sede_id'] = self.sede_id

        detalles = DetallePedido.objects.filter(**filtros).select_related('producto__sede')

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

        if not rows:
            return pd.DataFrame(columns=[
                'id_producto','nombre_producto','cantidad',
                'valor_compra','valor_venta','ganancia','sede_nombre'
            ])

        df = pd.DataFrame(rows)
        agg = df.groupby(
            ['sede_id','sede_nombre','id_producto','nombre_producto'],
            as_index=False
        ).agg({'cantidad':'sum','precio_compra':'first','precio_venta':'first'})

        agg['valor_compra'] = agg['precio_compra'] * agg['cantidad']
        agg['valor_venta']  = agg['precio_venta']  * agg['cantidad']
        agg['ganancia']     = agg['valor_venta']   - agg['valor_compra']

        return agg[[
            'id_producto','nombre_producto','cantidad',
            'valor_compra','valor_venta','ganancia','sede_nombre'
        ]]
    
    def to_excel(self, df: pd.DataFrame) -> BytesIO:
        from io import BytesIO
        import pandas as pd

        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Reporte')
        output.seek(0)
        return output
