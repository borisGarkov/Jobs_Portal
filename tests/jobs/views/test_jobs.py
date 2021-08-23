from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from jobs_portal.jobs.models import JobModel

UserModel = get_user_model()


class TestJobViews(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = UserModel.objects.create_user(email='test@abv.bg', password='123456')

    def test_newUser_hasNoJobsAdded(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('profile', args=[self.user.id]))

        jobs_posted = list(response.context['jobs'])
        self.assertEqual([], jobs_posted)
        self.assertTemplateUsed(response, 'profile/profile.html')

    def test_newUser_hasOneJobAdded(self):
        self.client.force_login(self.user)
        job_posted = JobModel.objects.create(
            title='title',
            description='description',
            city='Sofia',
            salary=50,
            user_id=self.user.id
        )
        response = self.client.get(reverse('profile', args=[self.user.id]))

        all_jobs = list(response.context['jobs'])
        self.assertEqual(1, len(all_jobs))
        self.assertTemplateUsed(response, template_name='profile/profile.html')

    def test_user_deletesJob(self):
        self.client.force_login(self.user)
        job_posted = JobModel.objects.create(
            title='title',
            description='description',
            city='Sofia',
            salary=50,
            user_id=self.user.id
        )
        job_posted.delete()
        response = self.client.get(reverse('profile', args=[self.user.id]))

        all_jobs = list(response.context['jobs'])
        self.assertEqual(0, len(all_jobs))
        self.assertTemplateUsed(response, template_name='profile/profile.html')

    def test_mainPageContainsOneJobPost(self):
        self.client.force_login(self.user)
        job_posted = JobModel.objects.create(
            title='title',
            description='description',
            city='Sofia',
            salary=50,
            user_id=self.user.id
        )

        response = self.client.get(reverse('home'))
        all_jobs = list(response.context['jobs'])
        self.assertEqual(1, len(all_jobs))
        self.assertTemplateUsed(response, template_name='home.html')
