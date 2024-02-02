from django.db import models
from authentication.models import Employee
from authentication.choices import TASK_STATUS
# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    assigned_to = models.ManyToManyField(Employee)
    due_date = models.DateField()
    status = models.CharField(max_length=50, choices=TASK_STATUS)
    
    def __str__(self) -> str:
        return self.title