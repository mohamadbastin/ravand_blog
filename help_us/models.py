from django.db import models


# Create your models here.

class WorkRequest(models.Model):
    name = models.CharField(max_length=1020)
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=1024)
    age = models.PositiveIntegerField()
    location = models.CharField(max_length=10000)
    education = models.TextField(max_length=12033)
    skills = models.TextField(max_length=23433)
    why = models.TextField(max_length=24443, null=True, blank=True)
    departments = models.TextField(max_length=32432)
    resume = models.FileField(null=True, blank=True)
    date = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name
