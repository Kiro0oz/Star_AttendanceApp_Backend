from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import AttendanceRecord
from .resources import AttendanceRecordResource

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(ImportExportModelAdmin):
    resource_class = AttendanceRecordResource

    

    list_display = (
        'user_name',        
        'committee_name',   
        'session_name',     
        'check_in_time',    
        'status',           
        'is_registered',    
    )
    

    search_fields = ('user__username', 'user__first_name', 'session__name')
    

    list_filter = ('session__committee', 'status', 'session__name', 'check_in_time')
    
    ordering = ('-check_in_time',)

    
    @admin.display(description='Member Name')
    def user_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    
    @admin.display(description='Session Name')
    def session_name(self, obj):
        return obj.session.name
    
    @admin.display(description='Committee')
    def committee_name(self, obj):
        return obj.session.get_committee_display()
    
    @admin.display(boolean=True, description='Registered')
    def is_registered(self, obj):
        return True 
    
   
    def has_change_permission(self, request, obj=None):
     
        return request.user.is_superuser
    
    readonly_fields = ('user', 'session', 'check_in_time', 'status')