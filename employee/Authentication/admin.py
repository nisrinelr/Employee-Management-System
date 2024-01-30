from django.contrib import admin
from .models import Departement, Employee
# Register your models here.

class SimpleAccountAdmin(admin.ModelAdmin):



    list_display = ('username', 'email', 'phone_number',)
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_number',)


    fields = (
        'email',
        'username',
        'first_name',
        'last_name',
        'phone_number',
        'address',
        'department',
    )
admin.site.register(Employee, SimpleAccountAdmin)
admin.site.register(Departement)