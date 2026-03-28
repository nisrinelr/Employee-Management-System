from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from authentication.serializers import AttendanceSerializer
from rest_framework.views import APIView
from rest_framework import generics
from attendance.models import Attendance
from authentication.models import Notification
from authentication.permissions import IsEmployee, IsHRManager, IsSuperadmin
# Create your views here.


def login_view(request):
    """Custom login view for the Employee Management System."""
    # Redirect already-authenticated users to admin
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            return render(request, 'authentication/login.html', {
                'error': 'Please enter both username and password.',
                'username': username,
            })

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect to 'next' param or admin dashboard
            next_url = request.POST.get('next') or request.GET.get('next') or '/'
            return redirect(next_url)
        else:
            return render(request, 'authentication/login.html', {
                'error': 'Invalid username or password. Please try again.',
                'username': username,
            })

    # GET request — pass the 'next' parameter to the template
    return render(request, 'authentication/login.html', {
        'next': request.GET.get('next', ''),
    })

class AttendanceView(generics.CreateAPIView):
    permission_classes = [IsSuperadmin, IsHRManager, IsEmployee]
    serializer_class = AttendanceSerializer
    queryset = Attendance.objects.all()
    
    def post(self, request, *args, **kwargs):
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return super().post(request, *args, **kwargs)


def notifications(request):
    notifications = Notification.filter(recipient=request.user)
    print('notifications',notifications)
    return render(request,'_main_header.html',{'notifications': notifications})