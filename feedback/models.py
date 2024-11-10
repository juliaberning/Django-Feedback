from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    manager = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="employees")
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
        return f'{self.user},{self.department}'
    
class FeedbackProcess(models.Model):
    reviewee = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="reviews_received")
    manager = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name="managed_feedback_processes")
    creation_date = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    feedback_process = models.ForeignKey(FeedbackProcess, on_delete=models.CASCADE, related_name="review")
    reviewer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name="reviews_given")
    reviewee_strengths_text= models.TextField(blank=True, null=True)
    reviewee_improvements_text = models.TextField(blank=True, null=True)
    GROWTH_CHOICES = [
    (1, 'Lacks initiative for growth, no improvement effort'),
    (2, 'Occasionally seeks growth but lacks consistency'),
    (3, 'Actively seeks learning and shows progress'),
    (4, 'Regularly challenges themselves, takes initiative'),
    (5, 'Proactively seeks growth, mentors others')
    ]  
    EXECUTION_CHOICES = [
    (1, 'Avoids change, struggles to deliver'),
    (2, 'Open to ideas but execution is inconsistent'),
    (3, 'Contributes to innovation and delivers results'),
    (4, 'Leads innovation, consistently drives impactful outcomes'),
    (5, 'Champions bold change, consistently exceeds expectations')
    ]
    COLLABORATION_CHOICES = [
    (1, 'Works alone, avoids teamwork'),
    (2, 'Participates when needed, limited communication'),
    (3, 'Actively collaborates and communicates effectively'),
    (4, 'Highly collaborative, fosters positive team dynamics'),
    (5, 'Leads collaboration, elevates team performance')
    ]
    reviewee_growth_rating = models.IntegerField(blank=True,null=True, choices=GROWTH_CHOICES)
    reviewee_execution_rating = models.IntegerField(blank=True, null=True,choices=EXECUTION_CHOICES)
    reviewee_collaboration_rating = models.IntegerField(blank=True, null=True,choices=COLLABORATION_CHOICES)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['reviewer', 'feedback_process'], name='unique_reviewer_feedback_process')
        ]