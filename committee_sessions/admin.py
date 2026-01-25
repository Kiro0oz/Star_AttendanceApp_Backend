from django.contrib import admin
from django.utils import timezone
from .models import Session
from import_export.admin import ImportExportModelAdmin
from .resources import SessionResource

class ActiveSessionFilter(admin.SimpleListFilter):
    title = 'Active Status'
    parameter_name = 'active_status'

    def lookups(self, request, model_admin):
        return (
            ('active', 'Active Now'),
            ('upcoming', 'Upcoming'),
            ('ended', 'Ended'),
        )

    def queryset(self, request, queryset):
        now = timezone.now()
        if self.value() == 'active':
            return queryset.filter(start_time__lte=now, end_time__gte=now)
        if self.value() == 'upcoming':
            return queryset.filter(start_time__gt=now)
        if self.value() == 'ended':
            return queryset.filter(end_time__lt=now)
        return queryset

@admin.register(Session)
class SessionAdmin(ImportExportModelAdmin):
    resource_class = SessionResource
    list_display = (
        'name', 
        'committee', 
        'start_time', 
        'end_time',
        'is_active', 
        'manual_code', 
        'instructor'
    )
    
    search_fields = ('name', 'instructor', 'manual_code')
    
    list_filter = (ActiveSessionFilter, 'committee', 'start_time', 'end_time')
    
    list_editable = ('start_time', 'end_time', 'manual_code')
    
    ordering = ('-start_time',)

    @admin.display(boolean=True, description='Active Now')
    def is_active(self, obj):
        now = timezone.now()
        return obj.start_time <= now <= obj.end_time