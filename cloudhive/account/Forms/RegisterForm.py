from django import forms
from account.models import users_temporal
class RegisterForm(forms.Form):
    ROLES = (
        ('admin', 'Administrador'),
        ('mesero', 'Mesero'),
        ('cajero', 'Cajero'),
    )

    name = forms.CharField(label='Nombre completo', max_length=100)
    email = forms.EmailField(label='Correo electrónico', max_length=100)
    pwd = forms.CharField(label='Contraseña', widget=forms.PasswordInput, max_length=100)
    rol = forms.ChoiceField(label='Rol de usuario', choices=ROLES)
    
    def save(self):
        users_temporal.objets.create(
            name = self.cleaned_data['name'],
            email = self.cleaned_data['email'],
            pwd = self.cleaned_data['pwd'],
            rol = self.cleaned_data['rol'],
        )