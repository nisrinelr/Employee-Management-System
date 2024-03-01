from django.urls import path
from authentication.views import AttendanceView

urlpatterns = [
    path('attendances/', AttendanceView.as_view(), name='attendance'),
]
