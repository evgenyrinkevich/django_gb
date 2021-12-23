from PIL import Image
from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class ShopUser(AbstractUser):
    age = models.PositiveIntegerField(null=True)
    avatar = models.ImageField(upload_to='users_avatar', blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.avatar:
            img = Image.open(self.avatar.path)
            if img.height > 350 or img.width > 350:
                new_img = (350, 350)
                img.thumbnail(new_img)
                img.save(self.avatar.path)

    def send_verify_mail(self):
        verify_link = '<verify_link>'
        # verify_link = reverse('auth:verify', args=[self.email, self.activation_key])
        subject = f'Confirm {self.username}'
        message = f'To confirm {self.username} on web-site ' \
                  f'{settings.DOMAIN_NAME} click: \n{settings.DOMAIN_NAME}{verify_link} '

        return send_mail(subject, message, settings.EMAIL_HOST_USER, [self.email], fail_silently=False)