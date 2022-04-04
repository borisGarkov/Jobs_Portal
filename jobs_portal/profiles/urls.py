from django.contrib.auth.views import PasswordChangeView
from django.urls import path
import jobs_portal.profiles.signals
from jobs_portal.profiles.views import ShowProfilePage, UpdateProfilePage, DeleteProfile, PasswordChange

urlpatterns = [
    path('<slug:slug>/', ShowProfilePage.as_view(), name='profile'),
    path('<slug:slug>/edit-profile', UpdateProfilePage.as_view(), name='edit profile'),
    path('<slug:slug>/delete-profile', DeleteProfile.as_view(), name='delete profile'),
    path('password/', PasswordChange.as_view(), name='password'),
]