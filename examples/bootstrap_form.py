# フォームクラスに対して、forms.Formの代わりにBaseFormを継承するように変更します。
# そうすると、as_floating()やas_controls()を使用できます。

# forms.py
from django import forms
from core.forms import BaseForm

# BaseFormクラス
class CustomForm(BaseForm): # ← ここの継承元を変更
    name = forms.CharField(verbose_name='お名前')
    email = forms.EmailField(verbose_name='メールアドレス')
    message = forms.CharField(verbose_name='メッセージ', widget=forms.Textarea)



# views.py
from django.shortcuts import render
from django.views.generic.edit import FormView
# from .forms import CustomForm

class CustomFormView(FormView):
    form_class = CustomForm
    template_name = 'form.html'
    success_url = '/'

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)
