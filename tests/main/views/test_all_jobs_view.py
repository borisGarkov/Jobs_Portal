from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from jobs_portal.jobs.models import JobModel

UserModel = get_user_model()


class TestMainViews(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_allJobsView_ExpectLenOfSix(self):
        response = self.client.get(reverse('search jobs'))
        categories_length = len(response.context['categories'])
        self.assertEqual(6, categories_length)

    def test_mainPageNumberOfJobs_expectZero(self):
        response = self.client.get(reverse('home'))
        jobs_length = len(response.context['jobs'])
        self.assertEqual(0, jobs_length)

    def test_mainPageNumberOfJobs_expectOne(self):
        self.user = UserModel.objects.create_user(email='boris.garkov@abv.bg', password='123456')
        self.user.is_active = True
        self.user.save()

        self.job_posted = JobModel.objects.create(
            title='title',
            description='description',
            city='Sofia',
            salary=50,
            user_id=self.user.id
        )

        response = self.client.get(reverse('home'))
        jobs_length = len(response.context['jobs'])
        self.assertEqual(1, jobs_length)
