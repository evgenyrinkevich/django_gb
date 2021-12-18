from PIL import Image
from django.db import models
from django.contrib.auth.models import AbstractUser


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

