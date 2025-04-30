# adminis/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import Usuario

class UsuarioForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        # Incluimos también 'rol', 'estado' y 'sede'
        fields = [
            'nombres', 'apellidos', 'tipoDocumento',
            'numDocumento', 'correo',
            'rol', 'estado', 'sede',
            'password1', 'password2'
        ]
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'tipoDocumento': forms.Select(attrs={'class': 'form-select'}),
            'numDocumento': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'sede': forms.Select(attrs={'class': 'form-select'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        # Asignar username igual al correo
        user.username = self.cleaned_data['correo']
        if commit:
            user.save()
        return user
