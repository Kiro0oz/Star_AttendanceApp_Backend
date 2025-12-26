from django.contrib import admin
from .models import Session

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = (
        'name', 
        'committee', 
        'start_time', 
        'end_time', 
        'manual_code', 
        'instructor'
    )
    
    search_fields = ('name', 'instructor', 'manual_code')
    
    list_filter = ('committee', 'start_time', 'end_time')
    
    list_editable = ('start_time', 'end_time', 'manual_code')
    
    ordering = ('-start_time',)