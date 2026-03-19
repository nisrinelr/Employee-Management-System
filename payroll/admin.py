from django.contrib import admin
from .models import Deduction, Country , PayrollReport, Allowences
from authentication.models import Employee
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, Spacer

class DeductionInline(admin.TabularInline):
    model = Deduction
class AllowenceInline(admin.TabularInline):
    model = Allowences
class PayrollAdmin(admin.ModelAdmin):
    list_display = ('country', 'salary', 'net_salary')
    inlines = [DeductionInline]

    def net_salary(self, obj):
        total_deductions = sum(d.amount for d in obj.deduction_set.all())
        tax_rate = obj.country.tax_rate
        tax_amount = obj.salary * tax_rate
        net_salary = obj.salary - tax_amount - total_deductions
        return net_salary

    net_salary.short_description = 'Net Salary'
    
@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'tax_rate')


class PayrollReportAdmin(admin.ModelAdmin):
    list_display = ('employee', 'month', 'year', 'country', 'net_salary')
    list_filter = ('month', 'year', 'country')
    search_fields = ('employee__username', 'employee__first_name', 'employee__last_name')
    actions = ['generate_payroll_pdf']

    def generate_payroll_pdf(self, request, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="payroll_reports.pdf"'

        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        style_heading = styles['Heading1']

        for obj in queryset:
            elements.append(Paragraph(f"Payroll Report: {obj.employee.username}", style_heading))
            elements.append(Spacer(1, 15))

            data = [
                ['Employee', str(obj.employee.username)],
                ['Month/Year', f"{obj.month}/{obj.year}"],
                ['Country', str(obj.country.name)],
                ['Base Salary', str(getattr(obj.employee, 'salary', 0))],
                ['Total Allowances', str(sum(a.amount for a in obj.allowences.all()))],
                ['Total Deductions', str(sum(d.amount for d in obj.deductions.all()))],
                ['Net Salary', str(obj.net_salary)],
            ]
            
            t = Table(data, style=[('GRID', (0, 0), (-1, -1), 1, colors.black), ('ALIGN', (0, 0), (-1, -1), 'LEFT')])
            elements.append(t)
            elements.append(Spacer(1, 30))

        doc.build(elements)
        return response

    generate_payroll_pdf.short_description = "Generate PDF for selected payroll reports"

    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(employee=request.user)
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.employee = request.user
        obj.save()

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.calculate_net_salary()


    def get_deductions(self, obj):
        return ", ".join([deduction.name for deduction in obj.deductions.all()])
    get_deductions.short_description = 'Deductions'
    def get_allowences(self, obj):
        return ", ".join([allowence.name for allowence in obj.allowences.all()])
    get_allowences.short_description = 'Allowences'

admin.site.register(PayrollReport, PayrollReportAdmin)
admin.site.register(Deduction)
admin.site.register(Allowences)