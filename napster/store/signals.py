from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Customer



@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
	if created:
		Customer.objects.create(user=instance, name = instance.first_name, email=instance.email)

