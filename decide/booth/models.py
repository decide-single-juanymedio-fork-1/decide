from django.db import models

class form(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, default="ejemplo@email.com")
    password1 = models.CharField(max_length=50)
    password2 = models.CharField(max_length=50)

