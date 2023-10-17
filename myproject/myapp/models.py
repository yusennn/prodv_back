from django.db import models
from django.contrib.auth.models import User

PRIORITY_CHOICES = [
    ('low', 'Низкий'),
    ('medium', 'Средний'),
    ('high', 'Высокий'),
]

STATUS_CHOICES = [
    ('new', 'New'),
    ('in_progress', 'In Progress'),
    ('resolved', 'Resolved'),
]


class Problem(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    actions = models.CharField(blank=True, max_length=1000)
    assigned_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_problems')
    resolved_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='resolved_problems')
