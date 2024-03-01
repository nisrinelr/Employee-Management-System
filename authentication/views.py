from django.shortcuts import render
from authentication.serializers import AttendanceSerializer
from rest_framework.views import APIView
from rest_framework import generics
from attendance.models import Attendance
from authentication.models import Notification
from authentication.permissions import IsEmployee, IsHRManager, IsSuperadmin
# Create your views here.

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