from django import forms
from django.core.mail import EmailMessage

from accounts.models import User
from bluebird import settings
from core.forms import BaseForm
from core.utils import send_teams_webhook

class ContactForm(BaseForm):
    name = forms.CharField(label='お名前', max_length=100)
    email = forms.EmailField(label='メールアドレス')
    subject = forms.CharField(label='件名', max_length=100)
    content = forms.CharField(label='内容', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # ユーザー情報を取得
        super(ContactForm, self).__init__(*args, **kwargs)

        # ユーザーがログインしている場合、初期値を設定
        if user and user.is_authenticated:
            self.fields['email'].initial = user.email
            self.fields['name'].initial = user.get_full_name() or user.username

    def send_email(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        subject = self.cleaned_data['subject']
        content = self.cleaned_data['content']

        mail_subject = f'Bluebirdお問い合わせ: {subject}'
        mail_body = '\n'.join([
            f'送信者: {name}',
            f'メールアドレス: {email}',
            'メッセージ:',
            content,
        ])

        # スタッフ権限を持つユーザーのメールアドレスを取得
        to_list = User.objects.filter(is_staff=True).exclude(email='').values_list('email', flat=True)
        to_list = list(to_list)

        message = EmailMessage(
            subject=mail_subject,
            body=mail_body,
            to=to_list,
        )

        message.send()

        if hasattr(settings, 'TEAMS_WEBHOOK_URL'):
            send_teams_webhook('お問い合わせがありました', {
                'お名前': name,
                'メールアドレス': email,
                '件名': subject,
                '内容': content,
            })

