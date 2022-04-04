from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, PermissionsMixin
from django.core.validators import validate_email
from django.db import models
from django_extensions.db.fields import AutoSlugField
from transliterate import translit


class AppUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class AppBaseUserModel(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': 'Потребител с този имейл вече съществува!',
        },
        validators=[validate_email],
    )

    username = models.CharField(
        max_length=25,
        unique=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    is_superuser = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=False,
    )

    slug = AutoSlugField(populate_from='username')

    date_joined = models.DateField(auto_now_add=True)

    USERNAME_FIELD = 'email'

    objects = AppUserManager()

    def __str__(self):
        return f'{self.email}'

    def slugify_function(self, content):
        '''
        first transliterate slug if it is in BG
        then if it contains multiple words, split by whitespace then join all words by '-'
        and finally check if '_' appears in the word and replace it with '-'
        '''
        content = translit(content, language_code='bg', reversed=True)
        return '-'.join(content.split()).replace('_', '-').lower()
