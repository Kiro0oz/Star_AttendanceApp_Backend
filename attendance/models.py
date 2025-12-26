from django.db import models
from Auth.models import User
from committee_sessions.models import Session 

class AttendanceRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendances')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='attendances')
    check_in_time = models.DateTimeField(auto_now_add=True)
    
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('late', 'Late'),
        ('absent', 'Absent'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    
    class Meta:
        unique_together = ('user', 'session')
        ordering = ['-check_in_time']

    def __str__(self):
        return f"{self.user.username} - {self.session.name} ({self.status})"