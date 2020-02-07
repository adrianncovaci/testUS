from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import Submission

class SumbissionForm(forms.ModelForm):
    
    class Meta:
        model = Submission
        fields = ('image', 'user', 'test')