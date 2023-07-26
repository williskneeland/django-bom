from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Part


@receiver(post_save, sender=Part)
def my_handler(sender, instance, **kwargs):
    print(instance)