from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('user/<int:pk>/', views.ProfileView.as_view(), name='profile'),
    path('user-search/', views.UserSearchView.as_view(), name='user_search'),

    # Settings
    path('settings/', RedirectView.as_view(url='profile'), name='settings'),
    path('settings/profile/', views.ProfileChangeView.as_view(), name='settings_profile'),
    path('settings/password/', views.PasswordChangeView.as_view(), name='settings_password'),

    # Authentication
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    # Sign up / Reset password
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset-done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
