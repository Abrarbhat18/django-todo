# base/forms.py

from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'complete', 'due_date', 'priority', 'category']

class PositionForm(forms.Form):
    position = forms.CharField()
