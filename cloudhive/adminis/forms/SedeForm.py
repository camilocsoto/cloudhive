from django import forms
from adminis.models import Sede

class SedeForm(forms.ModelForm):
    class Meta:
        model = Sede
        fields = ['nombre', 'estado', 'Ciudad']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'Ciudad': forms.Select(attrs={'class': 'form-select'}),
        }
