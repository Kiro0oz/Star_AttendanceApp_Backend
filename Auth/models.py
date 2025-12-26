from django.db import models
from django.contrib.auth.models import AbstractUser


ROLE_CHOICES = (
    ('admin', 'Admin'),
    ('member', 'Member'),
)

COMMITTEE_CHOICES = (
    ('front_committee', 'Frontend Committee'),
    ('back_committee', 'Backend Committee'),
    ('mobile_committee', 'Mobile Committee'),
    ('ai_committee', 'AI Committee'),
    ('uiux_committee', 'UI/UX Committee'),
    ('dataAnalysis_committee', 'Data Analysis Committee'),
)


class User(AbstractUser):
    role = models.CharField(
        max_length=10, 
        choices=ROLE_CHOICES, 
        default='member', 
        help_text='User role: member or admin (Committee Head)'
    )
    
    committee = models.CharField(
        max_length=50, 
        choices=COMMITTEE_CHOICES, 
        default=None, 
        null=True, 
        blank=True
    )
    
    phone_number = models.CharField(max_length=15, blank=True, null=True, unique=True)
    


    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"