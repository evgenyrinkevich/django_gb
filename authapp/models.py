from datetime import timedelta

from PIL import Image
from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.timezone import now

from geekshop.settings import ACTIVATION_KEY_TTL


class ShopUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, default=18)
    avatar = models.ImageField(upload_to='users_avatar', blank=True)
    activation_key = models.CharField(max_length=128, blank=True)

    def basket_total_cost(self):
        return sum(map(lambda x: x.product_cost, self.basket.all()))

    def basket_total_qty(self):
        return sum(map(lambda x: x.quantity, self.basket.all()))

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


class ShopUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'male'),
        (FEMALE, 'female'),
    )

    user = models.OneToOneField(ShopUser, primary_key=True, on_delete=models.CASCADE)
    tagline = models.CharField(verbose_name='tags', max_length=128, blank=True)
    about_me = models.TextField(max_length=512, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)