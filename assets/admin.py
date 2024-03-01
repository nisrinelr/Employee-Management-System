from django.contrib import admin
from .models import Asset
# Register your models here.

class AssetAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(recipient=request.user)
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.employee = request.user
        obj.save()

admin.site.register(Asset)