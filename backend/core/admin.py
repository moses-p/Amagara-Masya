from django.contrib import admin
from .models import CenterConfig

@admin.register(CenterConfig)
class CenterConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude', 'safe_radius_m')
    fields = ('name', 'latitude', 'longitude', 'safe_radius_m') 