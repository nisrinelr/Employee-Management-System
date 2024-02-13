from django.contrib import admin
from authentication.models import Employee
# Register your models here.



class SimpleAccountAdmin(admin.ModelAdmin):



    list_display = (
    'emp_id',
    'username',
    'first_name',
    'middle_name',
    'last_name',
    'parentage',
    'contact_number',
    'email',
    'gender',
    'address',
    'department',
    'employee_type',
    'date_of_hiring',
    'date_of_joining',
    'nationality',
    'passport_number',
    'national_id_residence_permit',
    'adhaar_number',
    'date_of_birth',
    'work_location',
    'profile_picture',
    'passport_front',
    'passport_back', 
    )
    list_filter = ('employee_type',)
    search_fields = ('username', 'email', 'first_name', 'last_name', 'emp_id',)


    fields = (
    'username',
    'first_name',
    'middle_name',
    'last_name',
    'parentage',
    'contact_number',
    'email',
    'gender',
    'address',
    'department',
    'employee_type',
    'date_of_hiring',
    'date_of_joining',
    'nationality',
    'passport_number',
    'national_id_residence_permit',
    'adhaar_number',
    'date_of_birth',
    'work_location',
    'profile_picture',
    'passport_front',
    'passport_back', 
)

   
admin.site.register(Employee, SimpleAccountAdmin)
