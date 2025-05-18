from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from .Forms import RegisterForm, LoginForm  
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeDoneView, PasswordChangeView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.mixins import LoginRequiredMixin # redirige a login si no está autenticado

class UserView(LoginRequiredMixin, TemplateView):
    #muestra info del usuario (temporal)
    template_name = "index.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        context['user'] = self.request.user #sesión del usuario
        return context

class SignUpView(CreateView):
    # registrar usuario
    form_class = RegisterForm  
    success_url = reverse_lazy("accounts:login")
    template_name = 'registration/register.html'  

class CustomLoginView(LoginView):
    # iniciar sesión
    form_class = LoginForm
    template_name = "registration/login.html"
    def get_success_url(self):
        user = self.request.user
        # redirige a la vista correspondiente según el rol del usuario
        if user.rol == 1:
            return reverse_lazy('adminis:list_sede')
        elif user.rol == 2:
            return reverse_lazy('cajero:lista_categorias')
        elif user.rol == 3:
            return reverse_lazy('accounts:user_view')
        return super().get_success_url()

class CustomLogoutView(LogoutView):
    # cerrar sesión
    next_page = reverse_lazy('accounts:logged_out') 
    
class LoggedOutView(TemplateView):
    # vista de cierre de sesión
    template_name = "registration/logout.html"
    
# -- reset password -- 

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'registration/password_change_form.html'
    success_url = reverse_lazy('accounts:password_change_done')

class CustomPasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'registration/password_change_done.html'

class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'