from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from authentication.models import Employee

class EmployeeBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            
            user = Employee.objects.get(username=username)
            if check_password(password, user.password):
                return user
            else:
                print("Password not matched:", password)
        except Employee.DoesNotExist:
            print("User not found y")
            return None

    def get_user(self, id):
        try:
            return Employee.objects.get(id=id)
        except Employee.DoesNotExist:
            print("User not found")
            return None
