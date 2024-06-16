from django.db import models
from django.contrib.auth.models import User

class UserActionLog(models.Model):
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('like', 'Like/Dislike'),
        ('comment_add', 'Add Comment'),
        ('comment_delete', 'Delete Comment'),
        ('post_create', 'Create Post'),
        ('post_delete', 'Delete Post'),
        ('subscribe', 'Subscribe/Unsubscribe'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_action_display()} at {self.timestamp}"
