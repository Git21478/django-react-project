from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
from .models import User, Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def send_welcome_message(sender, instance, created, **kwargs):
    if created:
        send_mail(
            f"Welcome, {instance.username}!",
            "Ваша регистрация успешно завершена.",
            "from@example.com",
            ["to@example.com"],
            fail_silently=False,
        )