from django import forms
from mesero.models import Mesa

class MesaForm(forms.ModelForm):
    class Meta:
        model = Mesa
        # excluimos 'sede' de los campos, la asignaremos en la vista
        fields = ['nombre', 'capacidad', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'capacidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }