from django.contrib.auth import get_user_model
from django.test import TestCase

from jobs_portal.profiles.forms import ProfileForm
from jobs_portal.profiles.models import ProfileModel

from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

UserModel = get_user_model()


class TestProfile(TestCase):
    def setUp(self) -> None:
        self.user = UserModel.objects.create(email='test@test.com', username='test', password='test')
        self.profile = self.user.profilemodel

    def test_createProfileModel_invalidProfession(self):
        profile = ProfileModel(
            user=self.user,
        )
        profile.save()

        profile_form = ProfileForm({'first_name': 'test',
                                    'last_name': 'test_last_name',
                                    'profession': 't',
                                    })

        self.assertFalse(profile_form.is_valid())

    def test_createProfileModel_validProfession(self):
        profile = ProfileModel(
            user=self.user,
        )
        profile.save()

        profile_form = ProfileForm({'first_name': 'test',
                                    'last_name': 'test_last_name',
                                    'profession': 'test-profession',
                                    })

        self.assertFalse(profile_form.is_valid())


class TestImageUpload(TestCase):
    im = Image.new(mode='RGB', size=(200, 200))
    im_io = BytesIO()
    im.save(im_io, 'JPEG')
    im_io.seek(0)
    image = InMemoryUploadedFile(im_io, None, 'random-name.jpg', 'image/jpeg', len(im_io.getvalue()), None)

    def test_successfulProfileCreateAndUploadImage(self):
        data = {
            'first_name': 'test',
            'last_name': 'test2',
        }
        file_dict = {'profile_photo': self.image}

        profile_form = ProfileForm(data=data, files=file_dict)
        self.assertTrue(profile_form.is_valid())
