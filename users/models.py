from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class CustomUser(AbstractUser):
    #can define custom fields for the model (beyond what AbstractUser comes with)
    slug = models.SlugField(unique=True, default="user_account_outdated")

#some fields that I plan on adding to CustomUser
    # first_name = models.TextField()
    # last_name = models.TextField()
    # bio = models.TextField(max_length=500)
    # #this is probably gonna be a bitch to get working
    # profile_picture = models.ImageField()
    # #type=model relationship; one user relationship to many other users
    # friend_list = models.ManyToOneRel()





    #overridden to include slug
    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super().save(*args, **kwargs)

    #needed for all models to know what to return by default
    def __str__(self):
        return self.username
