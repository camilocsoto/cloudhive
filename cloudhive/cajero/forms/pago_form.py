from django import forms
from cajero.models import MetodoPago

class ConfirmarPagoForm(forms.Form):
    metodo_pago = forms.ModelChoiceField(
        queryset=MetodoPago.objects.all(),
        label="Método de pago",
        required=True,
        empty_label="Seleccione un método"
    )