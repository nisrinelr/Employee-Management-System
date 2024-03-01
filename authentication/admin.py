from django.contrib import admin
from django.contrib.auth.decorators import permission_required
from authentication.models import Employee, Departement, Notification
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer
from attendance.models import Attendance
from assets.models import Asset
from tasks.models import Task
from authentication.permissions import IsHRManager, IsSuperadmin
from authentication.constants import SUPERADMIN, HRMANAGER, EMPLOYEE

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
    'salary',
    'date_of_hiring',
    'date_of_joining',
    'nationality',
    'passport_number',
    'national_id_residence_permit',
    'adhaar_number',
    'date_of_birth',
    'work_location',
    'user_type',
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
    'salary',
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
    'user_type',
)
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)
        
    
    def generate_pdf_user_info(modeladmin, request, queryset):
        if not request.user.is_authenticated or not request.user.user_type in [SUPERADMIN, HRMANAGER]:
            return HttpResponse("You don't have the permission to access this page.", status=403)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="{user.username}.pdf"'

        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []

        list_display_fields = modeladmin.get_list_display(request)
        
        styles = getSampleStyleSheet()
        style_normal = styles['BodyText']
        style_heading = styles['Heading1']

        style_user_info = ParagraphStyle(
            'UserInfo',
            parent=styles['Normal'],
            fontSize=12,
            textColor=colors.black,
            leftIndent=10,
            spaceAfter=10,
        )
        
        for user in queryset:
            elements.append(Paragraph("Employee Report for {}".format(user.username), style_heading))
            if user.profile_picture:
                profile_picture_path = f"profile_pictures/test.png"  # Replace with the actual path to profile pictures
                profile_picture = Image(profile_picture_path, width=100, height=100)
                elements.append(profile_picture)

            elements.append(Spacer(1, 20))
            for field in list_display_fields:
                if hasattr(user, field):
                    field_name = field.replace('_', ' ').capitalize()
                    value = getattr(user, field)
                    basic_info_table_data = [[field_name, value]]
                    basic_info_table = Table(basic_info_table_data, style=[('ALIGN', (0, 0), (-1, -1), 'LEFT')])
                    elements.append(basic_info_table)
                    elements.append(Spacer(1, 20))

            if user.passport_front and user.passport_back:
                passport_front_path = f"{user.passport_front}"
                passport_back_path = f"{user.passport_back}"
                passport_front = Image(passport_front_path, width=100, height=100)
                passport_back = Image(passport_back_path, width=100, height=100)
                elements.append(passport_front)
                elements.append(passport_back)

                elements.append(Spacer(1, 20))
                
            tasks_assigned = Task.objects.filter(assigned_to=user)
            if tasks_assigned.exists():
                tasks_data = [['Task', 'Status']]
                for task in tasks_assigned:
                    tasks_data.append([task.title, task.status])
                tasks_table = Table(tasks_data, style=[('GRID', (0, 0), (-1, -1), 1, colors.black)])
                elements.append(Paragraph("<b>Tasks Assigned:</b>", style_heading))
                elements.append(tasks_table)

            elements.append(Spacer(1, 20))
            assigned_assets = Asset.objects.filter(assigned_to=user)
            if assigned_assets.exists():
                elements.append(Paragraph("<br/>Assigned Assets:", style_heading))
                for asset in assigned_assets:
                    elements.append(Paragraph("- {}".format(asset.name), style_normal))

            attendance_records = Attendance.objects.filter(employee=user)
            if attendance_records.exists():
                attendance_data = [['Date', 'Status']]
                for attendance in attendance_records:
                    attendance_data.append([str(attendance.date), attendance.status])
                attendance_table = Table(attendance_data, style=[('GRID', (0, 0), (-1, -1), 1, colors.black)])
                elements.append(Paragraph("<b>Attendance:</b>", style_heading))
                elements.append(attendance_table)

            elements.append(Spacer(1, 20))  


            
            elements.append(Paragraph("<br/><br/><br/><br/>", style_normal))

        doc.build(elements)
        return response

    generate_pdf_user_info.short_description = "Generate PDF of selected users' info"
    admin.site.add_action(generate_pdf_user_info)




        
    def generate_offer_letter(modeladmin, request, queryset):
        if not request.user.is_authenticated or not request.user.user_type in ['SUPERUSER', 'HRMANAGER']:
            return HttpResponse("You don't have the permission to access this page.", status=403)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="offer_letter.pdf"'

        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []
        
        list_display_fields = modeladmin.get_list_display(request)

        title_style = ParagraphStyle(name='TitleStyle', fontSize=18, alignment=1)
        content_style = ParagraphStyle(name='ContentStyle', fontSize=12, alignment=0)

        elements.append(Paragraph("Offer Letter", title_style))
        elements.append(Spacer(1, 20))

        company_name = "Your Company Name"
        for user in queryset:
            elements.append(Paragraph("Dear {},\n".format(request.user.username), content_style))
            elements.append(Paragraph("We are pleased to offer you employment at {} as [position].".format(company_name), content_style))
            elements.append(Spacer(1, 20))
            elements.append(Paragraph("Please find attached the details of your employment including terms and conditions.", content_style))
            elements.append(Spacer(1, 20))
            elements.append(Paragraph("If you accept this offer, please sign and date this letter in the space provided below and return it to us by [date].", content_style))
            elements.append(Spacer(1, 20))
            elements.append(Paragraph("Sincerely,", content_style))
            elements.append(Paragraph("Your Name", content_style))
            elements.append(Paragraph("Title", content_style))
        doc.build(elements)
        return response

    generate_offer_letter.short_description = "generate ofer letter"
    admin.site.add_action(generate_offer_letter)
    
class NotificationAdmin(admin.ModelAdmin):

    list_display = ('sender', 'recipient', 'message', 'timestamp')
    list_filter = ('sender', 'recipient')
    search_fields = ('sender__username', 'recipient__username')
    fields = ('recipient', 'message')


    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(recipient=request.user)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.sender = request.user
        obj.save()

    
    
    
    
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Employee, SimpleAccountAdmin)
admin.site.register(Departement)
