from django import forms
from core.forms import BaseForm
from .models import Vote, VoteResult

# ユーザーが投票をつくるとき
class CreateVoteForm(forms.ModelForm, BaseForm):
    choices = forms.CharField(label='選択肢（行区切り）', widget=forms.Textarea)

    class Meta:
        model = Vote
        fields = ['title', 'description']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(CreateVoteForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        vote = super(CreateVoteForm, self).save(commit=False)
        vote.user = self.user
        vote.save()

        choices = self.cleaned_data['choices'].split('\n')
        for choice in choices:
            vote.choices.create(value=choice.strip())

        return vote

# 選択肢を選ぶとき
class SelectChoiceForm(forms.ModelForm, BaseForm):
    choice = forms.ModelChoiceField(queryset=None, widget=forms.RadioSelect)

    class Meta:
        model = VoteResult
        fields = []

    def __init__(self, *args, **kwargs):
        self.vote = kwargs.pop('vote')
        self.user = kwargs.pop('user')
        super(SelectChoiceForm, self).__init__(*args, **kwargs)
        self.fields['choice'].queryset = self.vote.choices.all()

    def save(self, commit=True):
        result = super(SelectChoiceForm, self).save(commit=False)
        result.user = self.user
        result.vote = self.vote
        result.choice = self.cleaned_data['choice']
        result.save()

        return result
