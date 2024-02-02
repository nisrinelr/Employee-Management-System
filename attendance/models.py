from django.db import models
from authentication.models import Employee
from authentication.choices import ATTENDANCE_STATUS
# Create your models here.

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=ATTENDANCE_STATUS)