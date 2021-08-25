from django.urls import path

from jobs_portal.main.views import HomeView, ContactsView, LookingForJobsView, search, PricingListView, AllJobsView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('search-jobs/', AllJobsView.as_view(), name='search jobs'),
    path('looking-for-jobs/', LookingForJobsView.as_view(), name='looking for jobs'),
    path('pricing-list/', PricingListView.as_view(), name='pricing-list'),
    path('search-all-page/', search, name='search all pages'),
]
