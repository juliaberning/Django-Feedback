from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="employees")
    DEPARTMENT_CHOICES = [
        ('AIA', 'AI Application'),
        ('MLE', 'ML Engineering'),
        ('MGMT', 'Management'),
        ('PM', 'Product Management'),
        ('SE', 'Software Engineering'),
        ('UXD', 'UX-Design'),
    ]

    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES, default='SE')

    
    def __str__(self):
        return f'{self.department}, {self.manager}'