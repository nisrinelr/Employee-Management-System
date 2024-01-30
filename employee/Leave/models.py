from django.db import models
from Authentication.models import Employee
from Authentication.choices import LEAVE_STATUS
# Create your models here.

class LeaveRequest(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=LEAVE_STATUS)
