from django.contrib.auth import get_user_model
from django.core.validators import validate_image_file_extension, MinLengthValidator
from django.db import models

from cloudinary.models import CloudinaryField

from utils.validate_image_extention import validate_img_extensions
from utils.validate_urls import is_string_an_url

UserModel = get_user_model()


class ProfileModel(models.Model):
    first_name = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        validators=[MinLengthValidator(2, 'Моля въведете поне 2 символа!')],
    )
    last_name = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        validators=[MinLengthValidator(2, 'Моля въведете поне 2 символа!')],
    )
    profile_photo = CloudinaryField(
        'image',
        folder='profile photos',
        validators=[validate_img_extensions],
    )
    profession = models.CharField(
        max_length=40,
        blank=True,
        null=True,
        validators=[MinLengthValidator(2, 'Моля въведете поне 2 символа!')],
    )
    website_url = models.URLField(
        max_length=255,
        blank=True,
        null=True,
        validators=[is_string_an_url],
    )
    facebook_url = models.URLField(
        max_length=255,
        blank=True,
        null=True,
        validators=[is_string_an_url],
    )
    instagram_url = models.URLField(
        max_length=255,
        blank=True,
        null=True,
        validators=[is_string_an_url],
    )
    twitter_url = models.URLField(
        max_length=255,
        blank=True,
        null=True,
        validators=[is_string_an_url],
    )
    user = models.OneToOneField(
        to=UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name} - User ({self.user})'
