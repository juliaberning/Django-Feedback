from django.db import models
from django.contrib.auth.models import User
# Create your models here.
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
class Review(models.Model):
    feedback_process = models.ForeignKey(FeedbackProcess, on_delete=models.CASCADE, related_name="review")
    reviewer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name="reviews_given")
    review_text = models.TextField()
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['reviewer', 'feedback_process'], name='unique_reviewer_feedback_process')
        ]