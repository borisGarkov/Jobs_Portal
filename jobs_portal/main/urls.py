from django.urls import path

from jobs_portal.main.views import HomeView, ContactsView, AllJobsPageView, search, PricingListView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('search-jobs/', AllJobsPageView.as_view(), name='search jobs'),
    path('pricing-list/', PricingListView.as_view(), name='pricing-list'),
    path('search-all-page/', search, name='search all pages'),
]
