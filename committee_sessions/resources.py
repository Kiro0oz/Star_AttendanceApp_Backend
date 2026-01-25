from import_export import resources
from .models import Session

class SessionResource(resources.ModelResource):
    class Meta:
        model = Session
        fields = ('id', 'committee', 'name', 'start_time', 'end_time', 'location', 'instructor', 'manual_code')
        export_order = ('id', 'name', 'committee', 'start_time', 'end_time', 'location', 'instructor', 'manual_code')
