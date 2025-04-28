from django.urls import path

from .views import producto_json
urlpatterns = [
    path('producto/', producto_json, name = "producto"),
]
