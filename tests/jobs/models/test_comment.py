from django.contrib.auth import get_user_model
from django.test import TestCase

from jobs_portal.jobs.models import JobModel, Comments

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

    def test_commentBody(self):
        self.client.force_login(self.user)
        comment_added = Comments.objects.create(
            comment='test comment',
            user_id=self.user.id,
            job_id=self.job_offer.id
        )

        self.assertEqual('test comment', comment_added.comment)
