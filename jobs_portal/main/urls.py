from django.urls import path

from jobs_portal.main.views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('business-clients/', BusinessClientsView.as_view(), name='business-clients'),
    path('search-jobs/', AllJobsView.as_view(), name='search jobs'),
    path('looking-for-jobs/', LookingForJobsView.as_view(), name='looking for jobs'),
    path('offer-jobs/', OfferJobsView.as_view(), name='offer jobs'),
    path('search-all-page/', search, name='search all pages'),
]
