from django.contrib.auth import get_user_model
from django.test import TestCase

from jobs_portal.jobs.forms import JobForm
from jobs_portal.profiles.forms import ProfileForm
from jobs_portal.profiles.models import ProfileModel

from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

UserModel = get_user_model()


class TestProfile(TestCase):
    im = Image.new(mode='RGB', size=(200, 200))
    im_io = BytesIO()
    im.save(im_io, 'JPEG')
    im_io.seek(0)
    image = InMemoryUploadedFile(im_io, None, 'random-name.jpg', 'image/jpeg', len(im_io.getvalue()), None)

    def setUp(self) -> None:
        self.user = UserModel.objects.create(email='test@test.com', username='test', password='test')
        self.profile = self.user.profilemodel

    def test_createJobModel_NegativeSalary(self):
        data = {
            'title': 'Test',
            'description': 'Test Description',
            'salary': -5,
            'user': self.user
        }

        file_dict = {
            'image': self.image
        }

        job_form = JobForm(data=data, files=file_dict)
        self.assertFalse(job_form.is_valid())

    def test_createJobModel_CategoryWhichIsNotListed(self):
        data = {
            'title': 'Test',
            'description': 'Test Description',
            'salary': 50,
            'work_category': 'Another',
            'user': self.user
        }

        file_dict = {
            'image': self.image
        }

        job_form = JobForm(data=data, files=file_dict)
        self.assertFalse(job_form.is_valid())

    def test_createJobModel_SalaryTypeWhichIsNotListed(self):
        data = {
            'title': 'Test',
            'description': 'Test Description',
            'salary': 50,
            'salary_type': 'Another',
            'user': self.user
        }

        file_dict = {
            'image': self.image
        }

        job_form = JobForm(data=data, files=file_dict)
        self.assertFalse(job_form.is_valid())
