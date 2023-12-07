from django.db import models

class form(models.Model):
    username = models.CharField(max_length=150)
    password1 = models.CharField(max_length=150)
    password2 = models.CharField(max_length=150)

