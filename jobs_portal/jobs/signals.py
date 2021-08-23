import cloudinary.uploader

from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver

from jobs_portal.jobs.models import JobModel


@receiver(pre_delete, sender=JobModel)
def delete_photo_when_user_deletes_account(sender, instance, **kwargs):
    try:
        picture_to_delete = instance.image
        cloudinary.uploader.destroy(picture_to_delete.public_id)
    except Exception:
        pass


@receiver(pre_save, sender=JobModel)
def photo_delete(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_picture = JobModel.objects.get(pk=instance.pk).image
        except JobModel.DoesNotExist:
            return
        else:
            try:
                new_picture = instance.image.public_id
            except Exception:
                new_picture = instance.image

            if old_picture and old_picture.public_id != new_picture:
                cloudinary.uploader.destroy(old_picture.public_id)
