from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from jobs_portal.jobs.models import JobModel

UserModel = get_user_model()


class TestMainViews(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_searchFunction_expectFindNothing(self):
        response = self.client.post(reverse('search all pages'), data={'searched': 'test'})
        result = response.context['result']
        self.assertEqual(0, len(result))

    def test_searchFunction_expectFindJob(self):
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

        response = self.client.post(reverse('search all pages'), data={'searched': 'description'})
        result = response.context['result']
        self.assertEqual(1, len(result))


