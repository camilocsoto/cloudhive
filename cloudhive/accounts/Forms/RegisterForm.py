from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import Usuario

class RegisterForm(UserCreationForm):

    nombres = forms.CharField(label="Nombre(s)")
    apellidos = forms.CharField(label="Apellido(s)")
    tipoDocumento = forms.ChoiceField(
        label="Tipo de documento",
        choices=Usuario.TYPEDOCS,
        widget=forms.Select(),
    )
    numDocumento = forms.CharField(label="Número de documento")
    correo = forms.EmailField( label="Correo electrónico",
        widget=forms.EmailInput(attrs={"autocomplete": "email"})
    )

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ["nombres","apellidos","tipoDocumento","numDocumento","correo", "password1","password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        # Asignar el username automáticamente desde el correo
        user.username = self.cleaned_data["correo"]
        if commit:
            user.save()
        return user