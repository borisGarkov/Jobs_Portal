from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


# Create your models here.
class Payments(models.Model):
    title = models.CharField(max_length=100, )
    price = models.IntegerField(default=0, )
    max_job_posts = models.IntegerField(default=0, )

    @property
    def display_price(self):
        return f'{self.price / 100:.2f}'

    def __str__(self):
        return f'{self.title}'


class UserSubscriptionPlan(models.Model):
    user = models.OneToOneField(
        to=UserModel,
        on_delete=models.CASCADE,
    )
    subscription_plan = models.ForeignKey(
        to=Payments,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.user} - {self.subscription_plan}'
