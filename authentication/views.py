from django.shortcuts import render

# Create your views here.
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from io import BytesIO
from django.http import FileResponse
from .models import Employee
from attendance.models import Attendance
from tasks.models import Task
from assets.models import Asset
from payroll.models import Salary

def generate_employee_report(request, employee_id):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    employee = Employee.objects.get(id=employee_id)
    attendance_data = Attendance.objects.filter(employee=employee)
    task_data = Task.objects.filter(employee=employee)
    asset_data = Asset.objects.filter(employee=employee)
    payroll_data = Salary.objects.filter(employee=employee)
    
    elements = []
    
    title_style = getSampleStyleSheet()['Heading1']
    title_style.alignment = 1
    title_text = f"Employee Report: {employee.username}"
    title = Paragraph(title_text, title_style)
    elements.append(title)
    elements.append(Spacer(1, 20))
    
    attendance_title = Paragraph("Attendance:", title_style)
    elements.append(attendance_title)
    attendance_table = generate_table_from_queryset(attendance_data)
    elements.append(attendance_table)
    elements.append(Spacer(1, 20))
    
    tasks_title = Paragraph("Tasks:", title_style)
    elements.append(tasks_title)
    tasks_table = generate_table_from_queryset(task_data)
    elements.append(tasks_table)
    elements.append(Spacer(1, 20))
    
    assets_title = Paragraph("Assets:", title_style)
    elements.append(assets_title)
    assets_table = generate_table_from_queryset(asset_data)
    elements.append(assets_table)
    elements.append(Spacer(1, 20))
    
    payroll_title = Paragraph("Payroll:", title_style)
    elements.append(payroll_title)
    payroll_table = generate_table_from_queryset(payroll_data)
    elements.append(payroll_table)
    elements.append(Spacer(1, 20))
    
    doc.build(elements)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f'employee_report_{employee.username}.pdf')

def generate_table_from_queryset(queryset):
    data = [[field.verbose_name for field in queryset.model._meta.fields]]
    for item in queryset:
        row = [str(getattr(item, field.name)) for field in queryset.model._meta.fields]
        data.append(row)
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), 'lightgrey'),
        ('TEXTCOLOR', (0, 0), (-1, 0), 'black'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), 'white'),
        ('GRID', (0, 0), (-1, -1), 1, 'black'),
    ]))
    return table