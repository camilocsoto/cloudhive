import pandas as pd
from django.utils.timezone import now
from io import BytesIO

from adminis.models import Sede
from cajero.models import Producto, DetallePedido

class SalesBySedeReport:
    """
    Genera un DataFrame con las columnas:
      - id_producto
      - nombre_producto
      - cantidad_producto (sumada por sede y producto)
      - valor_compra (precio_compra * cantidad)
      - valor_venta  (precio_venta  * cantidad)
      - ganancia     (valor_venta - valor_compra)
      - sede_nombre
    Agrupado por (sede, producto).
    """

    def build_dataframe(self):
        # Traer todos los detalles para pedidos completados
        detalles = DetallePedido.objects.filter(
            pedido__estado=1
        ).select_related('producto__sede')

        # Preparar lista de dicts
        rows = []
        for det in detalles:
            prod = det.producto
            sede = prod.sede
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

        # Agrupar por sede e ID de producto
        agg = df.groupby(
            ['sede_id', 'sede_nombre', 'id_producto', 'nombre_producto'],
            as_index=False
        ).agg({
            'cantidad'      : 'sum',
            'precio_compra' : 'first',   # ya es constante por producto
            'precio_venta'  : 'first',
        })

        # Calcular valores y ganancia
        agg['valor_compra'] = agg['precio_compra'] * agg['cantidad']
        agg['valor_venta']  = agg['precio_venta']  * agg['cantidad']
        agg['ganancia']     = agg['valor_venta']   - agg['valor_compra']

        # Reordenar columnas
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
        """
        Escribe el DataFrame a un BytesIO en formato Excel y lo devuelve.
        """
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Reporte')
        output.seek(0)
        return output
