from django.contrib import admin
from .models import Attendance
# Register your models here.

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee','date', 'status')
    list_filter = ('status',)
    search_fields = ('employee__username', 'date')
    fields = ('date', 'status')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(recipient=request.user)
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.employee = request.user
        obj.save()

# Register the model with admin site
admin.site.register(Attendance, AttendanceAdmin)