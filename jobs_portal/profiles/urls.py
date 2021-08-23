from django.contrib.auth.views import PasswordChangeView
from django.urls import path
import jobs_portal.profiles.signals
from jobs_portal.profiles.views import ShowProfilePage, UpdateProfilePage, DeleteProfile, PasswordChange

urlpatterns = [
    path('<int:pk>/', ShowProfilePage.as_view(), name='profile'),
    path('<int:pk>/edit-profile', UpdateProfilePage.as_view(), name='edit profile'),
    path('<int:pk>/delete-profile', DeleteProfile.as_view(), name='delete profile'),
    path('password/', PasswordChange.as_view(), name='password'),
]
