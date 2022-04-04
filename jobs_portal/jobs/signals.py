import cloudinary.uploader

from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from jobs_portal.jobs.models import JobModel


@receiver(post_save, sender=JobModel)
def send_email_when_job_created_to_verify(sender, instance, **kwargs):
    message = render_to_string('messages/send_job_verification_email.html', {
        'date_created': instance.date_posted,
        'job_id': instance.id,
        'job_title': instance.title,
        'job_user': instance.user.email,
    })

    default_email = 'rentahandbg@gmail.com'

    email = EmailMessage(
        subject='Please verify your job',
        body=message,
        from_email=default_email,
        to=[default_email, 'boris.garkov@abv.bg'],
    )

    email.send()


@receiver(pre_delete, sender=JobModel)
def delete_photo_when_user_deletes_account(sender, instance, **kwargs):
    try:
        picture_to_delete = instance.image
        cloudinary.uploader.destroy(picture_to_delete.public_id)
    except Exception:
        return


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
