from django.shortcuts import render
from .models import Mesa
from cajero.models import Producto, Pedido, DetallePedido
from django.http import JsonResponse
from django.utils import timezone

def lista_mesas(request):
    mesas = Mesa.objects.filter(sede=request.user.sede)
    productos = Producto.objects.filter(sede=request.user.sede) 


    print(productos)
    
    return render(request, "mesas/mesas.html", {
        "mesas": mesas,
        "productos": productos, 
    })

def ver_pedidos(request):
    mesa_id = request.GET.get('mesa_id')
    pedidos_pendientes = Pedido.objects.filter(mesa_id=mesa_id, estado=0)
    detalles = DetallePedido.objects.filter(pedido__in=pedidos_pendientes).select_related('producto')


    lista = [
        {
            'producto': detalle.producto.nombre,
            'cantidad': detalle.cantidad,
            'precio': float(detalle.producto.precio_venta),
        }
        for detalle in detalles
    ]

    mesa = Mesa.objects.get(id=mesa_id)

    return JsonResponse({
        'mesa': {
            'nombre': mesa.nombre,
            'estado': mesa.estado,
            'sede': mesa.sede.nombre
        },
        'pedidos': lista
    })

def agregar_producto_pedido(request):
    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        mesa_id = request.POST.get('mesa_id')

        mesa = Mesa.objects.get(id=mesa_id)
        mesa.estado = 1 
        mesa.save()

        try:
            producto = Producto.objects.get(id=producto_id)

            # Buscar o crear el pedido pendiente para esa mesa
            pedido, creado = Pedido.objects.get_or_create(
                mesa_id=mesa_id, estado=0,
                defaults={
                    'fecha_pedido': timezone.now(),
                    'pago_total': 0,
                    'metodo_pago_id': 1  # Asegúrate de tener un método de pago por defecto
                }
            )

            detalle, creado = DetallePedido.objects.get_or_create(
                pedido=pedido,
                producto=producto,
                defaults={'cantidad': 1}
            )

            if not creado:
                detalle.cantidad += 1
                detalle.save()

            return JsonResponse({'success': True, 'mensaje': 'Producto agregado al pedido'})
        except Producto.DoesNotExist:
            return JsonResponse({'success': False, 'mensaje': 'Producto no encontrado'})

    return JsonResponse({'success': False, 'mensaje': 'Método no permitido'})

def cancelar_mesa(request):
    mesa_id = request.POST.get("mesa_id")

    try:
        mesa = Mesa.objects.get(id=mesa_id)
        mesa.estado = 0 
        mesa.save()
        return JsonResponse({"success": True})
    except Mesa.DoesNotExist:
        return JsonResponse({"success": False, "error": "Mesa no encontrada"})
    

#Para entrar a la página ejecuta http://127.0.0.1:8000/mesero/producto/

