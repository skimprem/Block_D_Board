from django import forms
from django.core.exceptions import ValidationError
from adverts.models import Advert, Feedback
from django.contrib.auth.models import User

class AdvertForm(forms.ModelForm):
    class Meta:
        model = Advert
        fields = [
            'title',
            'category',
            'content',
        ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        text = cleaned_data.get('text')
        if text == title:
            raise ValidationError(
                {'text': 'Текст публикации не должен быть идентичен её названию'}
            )
        return cleaned_data

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback 
        fields = [
            'text',
        ]
