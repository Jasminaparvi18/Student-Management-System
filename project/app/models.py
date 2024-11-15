from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class user(AbstractUser):
    usertype=models.CharField(max_length=20)
    approve=models.IntegerField(blank=True,null=True)
    image=models.ImageField(upload_to='profile',null=True,blank=True)

class teacher(models.Model):
    teachid=models.ForeignKey(user,on_delete=models.CASCADE)
    name=models.CharField(max_length=20)
    age=models.IntegerField()
    email=models.EmailField()
    gender=models.CharField(max_length=10)
    department=models.CharField(max_length=20)

class student(models.Model):
    studid=models.ForeignKey(user,on_delete=models.CASCADE)
    name=models.CharField(max_length=20)
    age=models.IntegerField()
    email=models.EmailField()
    gender=models.CharField(max_length=10)