from django.db import models
from django.core.exceptions import ValidationError

class User(models.Model):
    id = models.AutoField(primary_key=True)
    telegram_id = models.CharField(max_length=64, unique=True, verbose_name="Telegram User ID")
    username = models.CharField(max_length=255, verbose_name="Username", null=True, blank=True)
    name = models.CharField(max_length=255, verbose_name="Full Name")
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name="Date Joined")
    
    ROLE_CHOICES = [
        ('boss', 'Boss'),
        ('admin', 'Admin'),
        ('user', 'Regular User'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user', verbose_name="User Role")
    
    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts", verbose_name="Author")
    title = models.CharField(max_length=255, verbose_name="Title")
    content = models.CharField(max_length=2048, verbose_name="Post Content")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date Created")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name="Post Status")

    def clean(self):
        additional_length = len(f"By {self.author.name}\\nPosted on {self.created_at:%Y-%m-%d %H:%M:%S}\\n")
        if len(self.content) + additional_length > 4096:
            raise ValidationError("Content is too long to send on Telegram.")

    def __str__(self):
        return f"Post: {self.title} ({self.status}) by {self.author.name} at {self.created_at}"

    class Meta:
        ordering = ['-created_at']
