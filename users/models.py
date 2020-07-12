from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify
from django.urls import reverse

#from community.models import Organization


class CustomUser(AbstractUser):
    #slug (and pk) allow custom urls for different users, groups, etc. -- slugs make the custom url more
    #       easily searchable through search engines because they are words, whereas pk's are numerical,
    #       both can be used together to make an even wider range of custom urls
    slug = models.SlugField(unique=True, default="user_account_outdated")

#some fields that I plan on adding to CustomUser
    # first_name = models.TextField()
    # last_name = models.TextField()
    # bio = models.TextField(max_length=500)
    # #this is probably gonna be a bitch to get working
    # profile_picture = models.ImageField()
    # #type=model relationship; one user relationship to many other users
    # friend_list = models.ManyToOneRel()
    # #also need to create a list of all the groups a user is a member of

    #list of all the groups a user is in
    #group_list = models.ManyToManyField(Organization)





    #overridden to include slug
    def save(self, *args, **kwargs):
        #slugify gets rid of spaces, makes it all lowercase, etc.
        self.slug = slugify(self.username)
        super().save(*args, **kwargs)

    #needed for all models to know what to return by default
    def __str__(self):
        return self.username
