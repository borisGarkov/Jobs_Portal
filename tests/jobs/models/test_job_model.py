from django.contrib.auth import get_user_model
from django.test import TestCase

from jobs_portal.jobs.models import JobModel

UserModel = get_user_model()


class JobModelTest(TestCase):
    def setUp(self) -> None:
        self.user = UserModel.objects.create_user(email='test@abv.bg', password='123456')
        self.job_offer = JobModel.objects.create(
            title='test',
            description='Test description',
            salary=50,
            image='path/image/test.jpg',
            user_id=self.user.id,
        )

    def test_initialJobSettings(self):
        self.assertEqual('test', self.job_offer.title)
        self.assertEqual('Test description', self.job_offer.description)
        self.assertEqual(50, self.job_offer.salary)
        self.assertEqual('path/image/test.jpg', self.job_offer.image)
        self.assertEqual('София', self.job_offer.city)
        self.assertEqual('на час', self.job_offer.salary_type)
        self.assertEqual('IT', self.job_offer.work_category)
        self.assertEqual(0, self.job_offer.total_likes())
