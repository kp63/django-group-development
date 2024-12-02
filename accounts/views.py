from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import views as auth_views, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import View, generic
from django.utils.decorators import method_decorator
from django.db.models import Q

from .decorators import guest_required

from .forms import SetPasswordForm, SignupForm, UpdateProfileForm, PasswordResetForm
from .models import User

# Create your views here.
class LoginView(auth_views.LoginView):
    template_name = 'accounts/auth/login.html'
    redirect_authenticated_user = True
    next_page = 'threads:index'

@method_decorator(guest_required, name='dispatch')
class SignupView(generic.CreateView):
    template_name = 'accounts/auth/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('threads:index')

    def form_valid(self, form):
        response = super().form_valid(form)

        # ユーザー登録と同時にログイン
        self.object = form.save()
        login(self.request, self.object)

        messages.success(self.request, 'ユーザー登録が完了しました🎉')

        return response
    
class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'accounts/auth/password_reset.html'
    email_template_name = "accounts/email/password_reset.html"
    success_url = reverse_lazy('accounts:password_reset_done')
    form_class = PasswordResetForm

    def form_valid(self, form):
        response = super().form_valid(form)

        return response

class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/auth/password_reset_done.html'


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/auth/password_reset_confirm.html'
    form_class = SetPasswordForm

    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        response = super().form_valid(form)

        messages.info(self.request, 'パスワードをリセットしました🔐')

        return response

class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'accounts/auth/logout.html')
        else:
            return redirect('threads:index')

    def post(self, request):
        logout(request)
        messages.info(request, 'ログアウトしました👋')

        return redirect('threads:index')

class ProfileView(generic.DetailView):
    model = User
    template_name = 'accounts/profile.html'

@method_decorator(login_required, name='dispatch')
class ProfileChangeView(generic.FormView):
    template_name = 'accounts/settings/profile.html'
    form_class = UpdateProfileForm
    success_url = reverse_lazy('accounts:settings')

    def form_valid(self, form: UpdateProfileForm):
        form.save()
        messages.info(self.request, 'プロフィールを更新しました👍')

        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        # initial['name'] = self.request.user.name
        # initial['bio'] = self.request.user.profile.bio


class PasswordChangeView(auth_views.PasswordChangeView):
    template_name = 'accounts/settings/password.html'
    form_class = SetPasswordForm
    success_url = reverse_lazy('accounts:settings')

    def form_valid(self, form):
        response = super().form_valid(form)

        messages.info(self.request, 'パスワードを変更しました🔐')

        return response

class UserSearchView(View):
    def get(self, request):
        query = request.GET.get('query')
        if query:
            users = User.objects.filter(Q(username__icontains=query) | Q(profile__bio__icontains=query))
        else:
            users = User.objects.none()

        return render(request, 'accounts/search.html', {'users': users, 'query': query})
