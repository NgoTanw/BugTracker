from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
	pic = models.ImageField(upload_to='img/', null=True)
	name = models.CharField(null=True, max_length=150)
	gender = models.CharField(null=True, max_length=15)
	dob = models.DateField(null=True, )
	mobile = models.CharField(null=True, max_length=10)
