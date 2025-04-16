from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from .Forms import RegisterForm, LoginForm  
from django.contrib.auth.views import LoginView

class UserView(TemplateView):
    template_name = "index.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userv = {
        'name': 'jon',
        'email': 'jondoe@gmail',
        'pwd': '1234',
        'rol': 'USER'
        }
        context['userv'] = userv
        return context

class SignUpView(CreateView):
    form_class = RegisterForm  
    success_url = reverse_lazy("login")
    template_name = 'registration/register.html'  

class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = "registration/login.html"
    def get_success_url(self):
        return reverse_lazy("user_view")