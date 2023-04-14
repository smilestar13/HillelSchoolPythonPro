from django import forms
from feedbacks.models import Feedback
import re


class FeedbackModelForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('user', 'text', 'rating')

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['user'].initial = user
        self.fields['rating'].help_text = "Rating should be from 1 to 5 💫"

    def clean(self):
        cleaned_data = super().clean()
        cleaned_text = cleaned_data.get('text', '')
        cleaned_text = re.sub(r'<[^>]*>|[^\w\s\']+', '', cleaned_text)
        cleaned_data['text'] = cleaned_text
        return cleaned_data
