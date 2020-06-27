from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify


class CustomUser(AbstractUser):
 #can define custom fields for the model (beyond what AbstractUser comes with)
    slug = models.SlugField(unique=True, default="user_account_outdated")

    #overridden to include slug
    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super().save(*args, **kwargs)


    #needed for all models to know what to return by default
    def __str__(self):
        return self.username
