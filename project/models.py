from django.db import models

# Create your models here.

class ProjectList(models.Model):
    ptitle = models.CharField(max_length = 100)
    ptype = models.CharField(max_length = 100)
    manager = models.CharField(max_length = 100)
    frontend = models.CharField(max_length = 100)
    backend = models.CharField(max_length = 100)
    client = models.CharField(max_length = 100)
    startdate = models.DateField()
    pstatus = models.CharField(max_length = 100)
    pdescription = models.TextField()