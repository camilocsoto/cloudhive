from django import forms
from adminis.models import Ciudad

class CiudadForm(forms.ModelForm):
    class Meta:
        model = Ciudad
        fields = ['nombre', 'estado', 'Pais']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'Pais': forms.Select(attrs={'class': 'form-select'}),
        }
