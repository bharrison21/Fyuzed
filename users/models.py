from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class CustomUser(AbstractUser):
    #slug (and pk) allow custom urls for different users, groups, etc. -- slugs make the custom url more
    #       easily searchable through search engines because they are words, whereas pk's are numerical,
    #       both can be used together to make an even wider range of custom urls
    slug = models.SlugField(unique=True, default="user_account_outdated")

#some fields that I plan on adding to CustomUser
    # first_name = models.TextField()
    # last_name = models.TextField()
    # bio = models.TextField(max_length=500)
    # profile_picture = models.ImageField()

    friend_list = models.ManyToManyField('CustomUser', related_name="friends")
    friend_requests = models.ManyToManyField('CustomUser', related_name="friendrequests")

    # could include links to other social medias / websites (i.e. twitter, linkedin, personal site)
    # personal_url = models.URLField(
    #     _("Personal URL"), max_length=555, blank=True, null=True
    # )

    #overridden to include slug
    def save(self, *args, **kwargs):
        #slugify gets rid of spaces, makes it all lowercase, etc.
        self.slug = slugify(self.username)
        super().save(*args, **kwargs)

    #needed for all models to know what to return by default
    def __str__(self):
        return self.username
