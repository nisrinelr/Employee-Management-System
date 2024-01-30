from django.db import models
from Authentication.models import Employee
# Create your models here.

class Asset(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    purchase_date = models.DateField()
    assigned_to = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
