from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
# Create your models here.

class Employee(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(blank=True, null=True)
    first_name = models.CharField(blank=True, null=True, max_length=25)
    last_name =  models.CharField(blank=True, null=True, max_length=25)
    phone_number = models.CharField(max_length=8,blank=True, null=True, validators=[RegexValidator(regex='^.{12}$', message='Length has to be 12')])
    address = models.CharField(max_length=100)
    department = models.ForeignKey("Departement", on_delete=models.CASCADE, null=True)
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []
    def __str__(self):
        return self.username

class Departement(models.Model):
    name = models.CharField(max_length=100)
    employees = models.ManyToManyField(Employee)
    capacity = models.IntegerField()