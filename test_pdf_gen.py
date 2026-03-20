import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "employee_manager.settings")
django.setup()
from authentication.models import Employee
from authentication.admin import SimpleAccountAdmin
from django.contrib.admin.sites import site
from django.test import RequestFactory
qs = Employee.objects.filter(username='admin')
admin_ins = SimpleAccountAdmin(Employee, site)
req = RequestFactory().get('/')
req.user = qs.first()
try:
    admin_ins.generate_pdf_user_info(req, qs)
    print("PDF Generation Succeeded")
except Exception as e:
    import traceback
    traceback.print_exc()
