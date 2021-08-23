from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path

from jobs_portal.job_auth.views import *

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('change-email-username/<int:pk>/', UpdateEmailUsernamePage.as_view(), name='change-email-username'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),

    path("password_reset", PasswordResetRequest.as_view(), name="password_reset"),

    path('password_reset/done/',
         PasswordResetDoneView.as_view(template_name='profile/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         PasswordResetConfirmViewCustom.as_view(template_name="profile/password_reset_confirm.html"),
         name='password_reset_confirm'),
    path('reset/done/',
         PasswordResetCompleteView.as_view(template_name='profile/password_reset_complete.html'),
         name='password_reset_complete'),
]
