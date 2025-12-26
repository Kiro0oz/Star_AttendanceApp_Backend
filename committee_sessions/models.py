from django.db import models
from Auth.models import User 
from Auth.models import COMMITTEE_CHOICES


class Session(models.Model):
    committee = models.CharField(
        max_length=50, 
        choices=COMMITTEE_CHOICES, 
        help_text="The committee this session belongs to."
    )
    name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=100, blank=True, null=True)
    instructor = models.CharField(max_length=100, blank=True, null=True)
    
    manual_code = models.CharField(max_length=8, unique=True, blank=True, null=True) 

    def __str__(self):
        return f"{self.name} - {self.committee} ({self.start_time.strftime('%Y-%m-%d %H:%M')})"