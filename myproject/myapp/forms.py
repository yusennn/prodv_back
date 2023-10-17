from django import forms
from .models import Problem
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


STATUS_CHOICES = [
    ('new', 'New'),
    ('in_progress', 'In Progress'),
    ('resolved', 'Resolved'),
    ('confirmed', 'Confirmed'),
]


class ProblemForm(forms.ModelForm):
    assigned_user = forms.ModelChoiceField(queryset=User.objects.filter(groups__name='Reception'))

    class Meta:
        model = Problem
        fields = ['name', 'phone', 'email', 'description', 'priority', 'status', 'assigned_user']


