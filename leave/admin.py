from django.contrib import admin
from .models import LeaveRequest
# Register your models here.

class LeaveAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'start_date', 'end_date', 'reason', 'is_approved')
    list_filter = ('leave_type', 'is_approved')
    search_fields = ('employee__username', 'employee__first_name', 'employee__last_name')
    fields = ('leave_type', 'start_date', 'end_date', 'reason')
    
    def approve_leave_request(self, request, queryset):
        if not request.user.is_authenticated or request.user.user_type not in ['HRMANAGER', 'SUPERUSER']:
            self.message_user(request, "You don't have permission to approve leave requests.", level='ERROR')
            return
        for leave_request in queryset:
            leave_request.is_approved = True
            leave_request.save()
        self.message_user(request, "Leave requests approved successfully.")

    approve_leave_request.short_description = "Approve selected leave requests"

    actions = [approve_leave_request]
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(employee=request.user)
    
    def save_model(self, request, obj, form, change):
        if obj.start_date >= obj.end_date:
            self.message_user(request, "Start date must be before end date.", level='ERROR')
            return
        if not change:
            obj.employee = request.user
        obj.save()
    
        
admin.site.register(LeaveRequest, LeaveAdmin)
