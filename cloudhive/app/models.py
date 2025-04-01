from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=60)
    rol = models.CharField(max_length=10)