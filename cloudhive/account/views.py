from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views import generic

from django.shortcuts import render
from .Forms import RegisterForm, LoginForm  # Importa los formularios

class UserView(TemplateView):
    template_name = "index.html"
    def get_context_data(self):
        userv = {
        'name': 'jon',
        'email': 'jondoe@gmail',
        'pwd': '1234',
        'rol': 'USER'
        }
        return {'userv':userv}

class RegisterFormView(generic.FormView):
    template_name = 'Auth/register.html'  # Cambia esto por la ruta de tu plantilla
    form_class = RegisterForm  

    def form_valid(self, form):
        # Aquí puedes manejar el formulario válido
        return super().form_valid(form)
    
    

def register_view(request):
    form = RegisterForm()
    return render(request, 'tu_template.html', {'form': form})

