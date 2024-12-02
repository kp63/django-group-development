from django import forms
from django.contrib.auth.forms import UserCreationForm,\
    PasswordResetForm as PasswordResetFormBase,\
    SetPasswordForm as SetPasswordFormBase

from core.forms import BaseForm

from .models import Profile, User


class SignupForm(UserCreationForm, BaseForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class UpdateProfileForm(forms.ModelForm, BaseForm): 
    # name = forms.CharField(label="表示名", max_length=30, required=True)
    bio = forms.CharField(label="自己紹介", max_length=500, required=False, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        user: User = self.instance

        if not user:
            raise ValueError("User instance is required")

        # if user.first_name != self.cleaned_data["name"]:
        #     user.first_name = self.cleaned_data["name"]

        profile, created = Profile.objects.get_or_create(user=user)

        if profile.bio != self.cleaned_data["bio"]:
            profile.bio = self.cleaned_data["bio"]
        
        if commit:
            user.save()
            profile.save()

        return user
    
    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        if kwargs.get('instance'):
            # self.fields['name'].initial = kwargs['instance'].first_name
            if hasattr(kwargs['instance'], 'profile'):
                self.fields['bio'].initial = kwargs['instance'].profile.bio

            self.fields['bio'].widget.attrs['rows'] = 5

    class Meta:
        model = User
        fields = []

class PasswordResetForm(PasswordResetFormBase, BaseForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['autofocus'] = True

class SetPasswordForm(SetPasswordFormBase, BaseForm):
    def __init__(self, *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)
        self.user = kwargs.pop('user')
        self.fields['new_password1'].widget.attrs['autofocus'] = True
    pass
