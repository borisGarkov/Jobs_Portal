import cloudinary.uploader
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver

from jobs_portal.job_auth.models import AppBaseUserModel
from jobs_portal.payments.models import UserSubscriptionPlan, Payments
from jobs_portal.profiles.models import ProfileModel


@receiver(post_save, sender=AppBaseUserModel)
def create_user(sender, created, instance, **kwargs):
    if created:
        profile = ProfileModel(
            user=instance
        )
        subscription = UserSubscriptionPlan(
            user=instance,
            subscription_plan=Payments.objects.get(pk=1),
        )

        picture = cloudinary.uploader.upload('anonymous-avatar-icon.jpg', folder='profile photos')
        profile.profile_photo = picture['public_id']
        profile.save()
        subscription.save()


@receiver(pre_delete, sender=ProfileModel)
def delete_photo_when_user_deletes_account(sender, instance, **kwargs):
    picture_to_delete = instance.profile_photo
    cloudinary.uploader.destroy(picture_to_delete.public_id)


@receiver(pre_save, sender=ProfileModel)
def photo_delete(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_picture = ProfileModel.objects.get(pk=instance.pk).profile_photo
        except ProfileModel.DoesNotExist:
            return
        else:
            try:
                new_picture = instance.profile_photo.public_id
            except Exception:
                new_picture = instance.profile_photo

            if old_picture and old_picture.public_id != new_picture:
                cloudinary.uploader.destroy(old_picture.public_id)
