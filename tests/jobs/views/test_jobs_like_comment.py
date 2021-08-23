from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse

from jobs_portal.jobs.models import JobModel, Comments

UserModel = get_user_model()


class TestJobViews(TestCase):
    def setUp(self) -> None:
        self.client = Client()
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

    def test_userLikesJob(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse('like job', kwargs={
            'pk': self.job_posted.id,
        }))

        like_exists = self.job_posted.likes.filter(user=self.user).exists()
        likes_count = self.job_posted.likes.count()

        self.assertTrue(like_exists)
        self.assertEqual(1, likes_count)

    def test_userLikesJobs_checkIfOtherUserDoesNotLikeTheJob(self):
        second_user = UserModel.objects.create_user(email='test2@abv.bg', password='qwerty123')
        second_user.is_active = True
        second_user.save()
        self.client.force_login(self.user)
        # self.client.force_login(second_user)

        response = self.client.post(reverse('like job', args=[self.job_posted.id]))

        like_exists = self.job_posted.likes.filter(user=second_user).exists()
        like_exists_by_first_user = self.job_posted.likes.filter(user=self.user).exists()
        likes_count = self.job_posted.likes.count()

        self.assertFalse(like_exists)
        self.assertTrue(like_exists_by_first_user)
        self.assertEqual(1, likes_count)

    def test_userAddsComment_invalidCommentExpected(self):
        self.client.force_login(self.user)

        with self.assertRaises(ValidationError) as exc:
            response = self.client.post(reverse('post comment', args=[self.job_posted.id]))
        self.assertEqual("['Невалиден коментар..']", str(exc.exception))

    def test_userAddsComment_validCommentExpected(self):
        self.client.force_login(self.user)
        comment_added = Comments.objects.create(
            comment='test comment',
            user_id=self.user.id,
            job_id=self.job_posted.id
        )

        comment_exists = self.job_posted.comments_set.filter(user=self.user).exists()
        comments_count = self.job_posted.comments_set.count()

        self.assertTrue(comment_exists)
        self.assertEqual(1, comments_count)

    def test_userAddsComment_validCommentExpectedThroughUrl(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('post comment', kwargs={'pk': self.job_posted.id}),
            data={'comment': 'test comment'}
        )

        comments_count = self.job_posted.comments_set.count()
        self.assertEqual(1, comments_count)

    def test_userDeletesComment(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('post comment', kwargs={'pk': self.job_posted.id}),
            data={'comment': 'test comment'}
        )

        comments_count = self.job_posted.comments_set.count()
        self.assertEqual(1, comments_count)

        current_comment = self.job_posted.comments_set.all()[0]

        response = self.client.post(
            reverse('delete comment', kwargs={'pk': current_comment.id}),
        )

        comments_count = self.job_posted.comments_set.count()

        self.assertEqual(0, comments_count)

    def test_userDeletesAnotherUserComment_expectFail(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('post comment', kwargs={'pk': self.job_posted.id}),
            data={'comment': 'test comment'}
        )

        second_user = UserModel.objects.create_user(email='test2@abv.bg', password='qwerty123')
        second_user.is_active = True
        second_user.save()

        is_comment_valid = self.job_posted.comments_set.filter(user=second_user).exists()
        is_comment_valid_original_user = self.job_posted.comments_set.filter(user=self.user).exists()

        self.assertFalse(is_comment_valid)
        self.assertTrue(is_comment_valid_original_user)
