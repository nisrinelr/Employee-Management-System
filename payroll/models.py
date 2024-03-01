from django.db import models
from authentication.models import Employee

class Country(models.Model):
    name = models.CharField(max_length=100)
    tax_rate = models.FloatField()

    def __str__(self):
        return self.name

class Deduction(models.Model):
    name = models.CharField(max_length=100)
    amount = models.FloatField()

    def __str__(self):
        return f"{self.name}"

class Allowences(models.Model):
    name = models.CharField(max_length=100)
    amount = models.FloatField()

    def __str__(self):
        return f"{self.name}"

class PayrollReport(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.IntegerField(choices=[(i, i) for i in range(1, 13)])
    year = models.IntegerField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    deductions = models.ManyToManyField(Deduction)
    allowences = models.ManyToManyField(Allowences)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.calculate_net_salary()
        
    def calculate_net_salary(self):
        total_allowances = sum(allowance.amount for allowance in self.allowances.all())
        total_deductions = sum(deduction.amount for deduction in self.deductions.all())
        self.net_salary = self.employee.salary + total_allowances - total_deductions
        self.save()
    
    

    