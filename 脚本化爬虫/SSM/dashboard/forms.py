# encoding=utf-8
from django.forms import ModelForm
from dashboard.models import Website, Task


class SiteForm(ModelForm):
    class Meta:
        model = Website
        exclude = ['id', 'status']


class TaskForm(ModelForm):
    class Meta:
        model = Task
        exclude = ['id', 'status']
