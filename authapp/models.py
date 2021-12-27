from datetime import timedelta

from PIL import Image
from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.timezone import now

from geekshop.settings import ACTIVATION_KEY_TTL


# def calc_activation_key_expires():
#     return now() + timedelta(hours=ACTIVATION_KEY_TTL)


class ShopUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, default=18)
    avatar = models.ImageField(upload_to='users_avatar', blank=True)
    activation_key = models.CharField(max_length=128, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.avatar:
            img = Image.open(self.avatar.path)
            if img.height > 350 or img.width > 350:
                new_img = (350, 350)
                img.thumbnail(new_img)
                img.save(self.avatar.path)

    def send_verify_mail(self):
        verify_link = reverse('auth:verify', kwargs={'email': self.email,
                                                     'activation_key': self.activation_key})

        subject = f'Confirm {self.username}'
        message = f'To confirm {self.username} on web-site ' \
                  f'{settings.DOMAIN_NAME} click: \n{settings.DOMAIN_NAME}{verify_link} '

        return send_mail(subject, message, settings.EMAIL_HOST_USER, [self.email], fail_silently=False)

    def is_activation_key_expired(self):
        return now() - self.date_joined > timedelta(hours=ACTIVATION_KEY_TTL)
