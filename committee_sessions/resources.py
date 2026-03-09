from import_export import resources
from import_export.fields import Field
from django.utils import timezone
from .models import Session

class SessionResource(resources.ModelResource):
    status = Field(column_name='Status')

    class Meta:
        model = Session
        fields = ('id', 'committee', 'name', 'level', 'start_time', 'end_time', 'location', 'instructor', 'manual_code', 'status')
        export_order = ('id', 'name', 'level', 'status', 'committee', 'start_time', 'end_time', 'location', 'instructor', 'manual_code')

    def dehydrate_status(self, session):
        now = timezone.now()
        if now < session.start_time:
            return "Upcoming"
        elif now > session.end_time:
            return "Ended"
        else:
            return "Active"
