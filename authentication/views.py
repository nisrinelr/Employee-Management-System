from django.shortcuts import render

# Create your views here.
from django.http import FileResponse
from .models import Employee
from attendance.models import Attendance
from tasks.models import Task
from assets.models import Asset
from payroll.models import Salary

