# threads/forms.py

from django import forms

from core.forms import BaseForm
from .models import ChatMessage, Thread

class ChatMessageForm(forms.ModelForm, BaseForm):
    class Meta:
        model = ChatMessage
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3, 'placeholder': 'メッセージを入力...'}),
        }

class CreateThreadForm(forms.ModelForm, BaseForm):
    class Meta:
        model = Thread
        fields = ['title']
