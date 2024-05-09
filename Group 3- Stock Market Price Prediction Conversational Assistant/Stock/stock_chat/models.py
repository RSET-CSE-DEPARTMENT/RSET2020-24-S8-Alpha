from django.db import models

# Create your models here.

class User(models.Model):
    uid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=150)
    contact = models.CharField(max_length=25)
