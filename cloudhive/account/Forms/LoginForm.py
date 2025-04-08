from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(label='Correo electrónico', max_length=100)
    pwd = forms.CharField(label='Contraseña', widget=forms.PasswordInput, max_length=100)