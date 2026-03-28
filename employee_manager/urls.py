from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from authentication.views import login_view

# Point Django admin's login to our custom login view
admin.site.login = login_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('', admin.site.urls),
    path('api/', include('authentication.urls')),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)