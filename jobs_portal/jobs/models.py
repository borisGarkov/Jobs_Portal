from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, validate_image_file_extension, MinLengthValidator
from django.db import models
from datetime import datetime

from utils.validate_image_extention import validate_img_extensions
from jobs_portal.profiles.models import ProfileModel

UserModel = get_user_model()


class JobModel(models.Model):
    WORK_CATEGORIES = [
        ('ИТ', 'ИТ'),
        ('Ремонтни Дейности', 'Ремонтни Дейности'),
        ('Монтажни Дейности', 'Монтажни Дейности'),
        ('Занаяти', 'Занаяти'),
        ('Поддръжка на автомобили', 'Поддръжка на автомобили'),
        ('Здраве и фитнес', 'Здраве и фитнес'),
        ('Транспорт и логистика', 'Транспорт и логистика'),
        ('Продажби, Маркетинг, ПР', 'Продажби, Маркетинг, ПР'),
        ('Финанси/Счетоводни услуги', 'Финанси/Счетоводни услуги'),
        ('Друго', 'Друго'),
    ]

    WORK_TYPE = [
        ('Търся Хора', 'Търся Хора'),
        ('Предлагам Услуга', 'Предлагам Услуга'),
    ]

    SALARY_TYPE = [
        ('на час', 'на час'),
        ('на месец', 'на месец'),
        ('по договаряне', 'по договаряне'),
    ]

    title = models.CharField(
        max_length=50,
        validators=[MinLengthValidator(2, 'Моля въведете поне 2 символа!')],
    )
    description = RichTextField()
    city = models.CharField(
        max_length=50,
        default='София',
        validators=[MinLengthValidator(2, 'Моля въведете поне 2 символа!')],
    )
    salary = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0)]
    )
    salary_type = models.CharField(
        max_length=50,
        choices=SALARY_TYPE,
        default='на час',
    )
    work_category = models.CharField(
        max_length=50,
        choices=WORK_CATEGORIES,
        default='IT'
    )
    work_type = models.CharField(
        max_length=50,
        choices=WORK_TYPE,
        default='Търся Хора'
    )
    image = CloudinaryField(
        'image',
        name='image',
        folder='job photos',
        validators=[validate_img_extensions],
    )
    last_modified = models.DateTimeField(
        auto_now=True,
    )
    date_posted = models.DateTimeField(
        auto_now_add=True
    )
    user = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
    )

    likes = models.ManyToManyField(ProfileModel, related_name='job_posts')

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f'{self.title} - {self.work_category}'


class Comments(models.Model):
    job = models.ForeignKey(JobModel, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    date_added = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f'Comment for {self.job}'

