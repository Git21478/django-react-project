from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail, EmailMultiAlternatives
from .models import User, Profile

from django.template.loader import render_to_string
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created

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

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    context = {
        "current_user": reset_password_token.user,
        "username": reset_password_token.user.username,
        "email": reset_password_token.user.email,
        "reset_password_url": "{}?token={}".format(
            # instance.request.build_absolute_uri(reverse("password-reset:reset-password-confirm")),
            "localhost:5173/password-reset/confirm/",
            reset_password_token.key)
    }

    email_html_message = render_to_string("email/user_reset_password.html", context)
    email_plaintext_message = render_to_string("email/user_reset_password.txt", context)

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()