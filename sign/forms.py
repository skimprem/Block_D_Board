from django import forms
from django.core.exceptions import ValidationError
from sign.models import OneTimeCode

class VerifyForm(forms.ModelForm):
    code = forms.CharField(label='Code', help_text='Enter Email verification')
    class Meta:
        model = OneTimeCode
        fields = [
            'code',
        ]
