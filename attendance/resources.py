from import_export import resources, fields
from .models import AttendanceRecord

class AttendanceRecordResource(resources.ModelResource):
    user_name = fields.Field(column_name='Member Name')
    session_name = fields.Field(attribute='session__name', column_name='Session')
    committee = fields.Field(column_name='Committee')
    status = fields.Field(column_name='Status')
    check_in_time = fields.Field(attribute='check_in_time', column_name='Check In Time')

    class Meta:
        model = AttendanceRecord
        fields = ('id', 'user_name', 'session_name', 'committee', 'check_in_time', 'status')
        export_order = ('id', 'user_name', 'session_name', 'committee', 'check_in_time', 'status')

    def dehydrate_user_name(self, attendance):
        return attendance.user.get_full_name() or attendance.user.username

    def dehydrate_committee(self, attendance):
        return attendance.session.get_committee_display()

    def dehydrate_status(self, attendance):
        return attendance.get_status_display()
