from django import forms
from .models import Question
from django.contrib.auth.models import User

class QuestionForm(forms.ModelForm):
    ask_to = forms.ModelChoiceField(queryset=User.objects.all(), label="質問するユーザー", required=True)

    class Meta:
        model = Question
        fields = ['ask_to', 'message']

