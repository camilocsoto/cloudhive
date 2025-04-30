from django import forms
from adminis.models import Pais

class PaisForm(forms.ModelForm):
    class Meta:
        model = Pais
        fields = ['Nombre', 'estado']
        widgets = {
            'Nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }
