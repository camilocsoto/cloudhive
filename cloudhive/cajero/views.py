from django.shortcuts import render

# Create your views here.

# Create your views here.
def producto_json(request):
    producto = {
        "nombre": "Botella de vino",
        "precio": 15.99
    }
    # Pasamos al contexto
    return render(request, "producto.html", {"producto": producto})
