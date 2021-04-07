from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Courses
from users.models import *
from django.core.mail import send_mail


@receiver(post_save,sender=Courses)
def send_update(sender,instance,created,**kwargs):
	if created:
		send_mail(from_mail='F20200930@pilani.bits-pilani.ac.in',
			to_emails=instance.taken_by.userr.email,
			subject=f'Update from{instance.created_by.creatorprofile.name} ',
			plain_text = f'{instance.created_by.creatorprofile.name} has just uploaded a new course!')

