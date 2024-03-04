import random
import string
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password
from authentication.choices import EMPLOYEE_TYPE , GENDER_CHOICES, USER_TYPE
# Create your models here.

class Employee(AbstractUser):
    emp_id = models.CharField(max_length=10, unique=True, editable=False, null=True)
    username = models.CharField(max_length=50, unique=True, null=True)
    first_name = models.CharField(max_length=50, null=True)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, null=True)
    parentage = models.CharField(max_length=100, null=True)
    contact_number = models.CharField(max_length=12,blank=True, null=True, validators=[RegexValidator(regex='^.{12}$', message='Length has to be 12')])
    email = models.EmailField(null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True)
    salary = models.FloatField()
    address = models.TextField(null=True)
    department = models.ForeignKey('Departement', on_delete = models.CASCADE, null=True)
    employee_type = models.CharField(max_length=20, choices=EMPLOYEE_TYPE, null=True)
    date_of_hiring = models.DateField(null=True)
    date_of_joining = models.DateField(null=True)
    nationality = models.CharField(max_length=50, null=True)
    passport_number = models.CharField(max_length=20, null=True)
    national_id_residence_permit = models.CharField(max_length=20, null=True)
    adhaar_number = models.CharField(max_length=12, blank=True, null=True)
    date_of_birth = models.DateField(null=True)
    work_location = models.CharField(max_length=100, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    passport_front = models.FileField(upload_to='passport_scans_front/', blank=True, null=True)
    passport_back = models.FileField(upload_to='passport_scans_back/', blank=True, null=True)
    user_type = models.CharField(max_length=100, choices=USER_TYPE, default=0)
    
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []
    
    def save(self, *args, **kwargs):
       emp_id_prefix = (self.username[:3]).lower()
       emp_id_suffix = ''.join(random.choices(string.digits, k=3))
       self.emp_id = f"{emp_id_prefix}-{emp_id_suffix}"
       self.password = make_password(self.username)
       super().save(*args, **kwargs)
    
    def __str__(self):
        return self.username

class Departement(models.Model):
    name = models.CharField(max_length=100)
    employees = models.ManyToManyField(Employee)
    capacity = models.IntegerField()
    
    def __str__(self):
        return self.name
    
    
class Notification(models.Model):
    sender = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='sent_notifications')
    recipient = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='received_notifications')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.recipient}: {self.message}"
