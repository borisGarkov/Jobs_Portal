from django.urls import path

from jobs_portal.main.views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('business-clients/', BusinessClientsView.as_view(), name='business-clients'),
    path('all-jobs/', JobsPageBaseView.as_view(), name='all jobs'),
    path('search-all-page/', search, name='search all pages'),
]
