from django.urls import path, include
from .views import generate_employee_report
from . import views
urlpatterns = [
    path('generateReport/<int:employee_id>', views.generate_employee_report, name='generateReports'),
    path('payslip/<int:pk>/', views.payslip, name='dashboard-payslip'),
]
