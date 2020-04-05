from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15)
    is_super = models.BooleanField()

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=1024)
    content = models.TextField(max_length=100000000000)
    category = models.ManyToManyField(Category, related_name='post')
    author = models.ForeignKey(Profile, related_name='post', on_delete=models.SET_NULL, null=True)
    picture = models.ImageField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.title + ' by ' + str(self.author)
