from django.db import models
from authentication.models import Employee
# Create your models here.

class Salary(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.15)

    def calculate_net_salary(self):
        net_salary = self.base_salary - (self.base_salary * self.tax_rate)
        return net_salary

    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name}'s Salary"