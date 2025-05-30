# cajero/forms.py (o donde corresponda)
from django import forms
from cajero.models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        # No incluimos 'sede' en el formulario, se inyecta desde la vista
        fields = ['nombre', 'stock', 'precio_compra', 'precio_venta', 'categoria', 'proveedor']
        widgets = {
            'nombre':         forms.TextInput(attrs={'class': 'form-control'}),
            'stock':          forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'precio_compra':  forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'precio_venta':   forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'categoria':      forms.Select(attrs={'class': 'form-select'}),
            'proveedor':      forms.Select(attrs={'class': 'form-select'}),
        }
