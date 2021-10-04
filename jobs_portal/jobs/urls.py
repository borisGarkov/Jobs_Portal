from django.urls import path

import jobs_portal.jobs.signals

from jobs_portal.jobs.views import CreateJob, JobDetails, like_job_post, UpdateJob, DeleteJob, post_comment, \
    delete_comment, JobApplicationView, JobConnectWithJobPosterView

urlpatterns = [
    path('create-job/', CreateJob.as_view(), name='create job'),
    path('update-job/<int:pk>/', UpdateJob.as_view(), name='update job'),
    path('delete-job/<int:pk>/delete', DeleteJob.as_view(), name='delete job'),
    path('details-job/<int:pk>/', JobDetails.as_view(), name='details job'),
    path('like/<int:pk>/', like_job_post, name='like job'),
    path('post-comment/<int:pk>/', post_comment, name='post comment'),
    path('delete-comment/<int:pk>/', delete_comment, name='delete comment'),
    path('apply/<int:pk>/', JobApplicationView.as_view(), name='apply'),
    path('connect/<int:pk>/', JobConnectWithJobPosterView.as_view(), name='connect'),
]
