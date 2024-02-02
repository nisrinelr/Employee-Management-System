from django.contrib import admin
from authentication.models import Employee
# Register your models here.



class SimpleAccountAdmin(admin.ModelAdmin):



    list_display = ('username', 'email', 'phone_number',)
    list_filter = ('employee_type', )
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_number',)


    fields = (
        'email',
        'username',
        'first_name',
        'last_name',
        'phone_number',
        'employee_type',
    )
   
#admin.site.register(Account)
admin.site.register(Employee, SimpleAccountAdmin)
