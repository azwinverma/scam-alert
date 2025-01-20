from django.db import models
from django.contrib.auth.models import User

class ScamReport(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='scam_images/', null=True, blank=True)  # Add this line


class Comment(models.Model):
    scam_report = models.ForeignKey(ScamReport, on_delete=models.CASCADE, related_name='comments')
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Ensure this field exists

    def __str__(self):
        return f"Comment by {self.commented_by.username} on {self.scam_report.title}"

class Reaction(models.Model):
    REACTION_CHOICES = [
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    ]
    scam_report = models.ForeignKey(ScamReport, on_delete=models.CASCADE, related_name='reactions')
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES)
    reacted_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.reaction_type} by {self.reacted_by.username} on {self.scam_report.title}"
