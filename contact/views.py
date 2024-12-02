from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import FormView

from .forms import ContactForm

# Create your views here.
class ContactFormView(FormView):
    template_name = 'contact/form.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact:form')

    # フォームにユーザー情報を渡す
    # （お問い合わせ者のメールアドレスを初期値として表示するため）
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form: ContactForm):
        form.send_email()

        messages.success(
            self.request,
            'お問い合わせを受け付けました。'
        )

        return super().form_valid(form)
