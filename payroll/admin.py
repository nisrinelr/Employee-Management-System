from django.contrib import admin
from .models import Deduction, Country , PayrollReport, Allowences
from authentication.models import Employee

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
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(employee=request.user)
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.employee = request.user
        obj.save()


    def get_deductions(self, obj):
        return ", ".join([deduction.name for deduction in obj.deductions.all()])
    get_deductions.short_description = 'Deductions'
    def get_allowences(self, obj):
        return ", ".join([allowence.name for allowence in obj.allowences.all()])
    get_allowences.short_description = 'Allowences'

admin.site.register(PayrollReport, PayrollReportAdmin)
admin.site.register(Deduction)
admin.site.register(Allowences)