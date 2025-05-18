"""
URL configuration for cloudhive project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import CustomLoginView, UserView, SignUpView, CustomLogoutView, LoggedOutView

app_name = 'accounts'
urlpatterns = [
    path('login/', CustomLoginView.as_view(), name = "login"),
    path('signup/', SignUpView.as_view(), name = "signup"),
    path('logout/', CustomLogoutView.as_view(), name = "logout"),
    path('logged-out/', LoggedOutView.as_view(), name='logged_out'), #redirect view
    path('profile/', UserView.as_view(), name = "user_view"),
]