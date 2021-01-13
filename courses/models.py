from django.db import models
from django.utils.text import slugify
import uuid


# == Both of these models need a slug or pk == 



class Listing(models.Model):
    name = models.CharField(max_length = 400, unique=True, default=uuid.uuid1)
    info = models.CharField(max_length = 400)

    slug = models.SlugField(unique=True, default=uuid.uuid1)

    @classmethod
    def create(cls, name, info):
        listing = cls(name, info)

    def save(self, *args, **kwargs):
        #slugify gets rid of spaces, makes it all lowercase, etc.
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return str(self.name)




class Course(models.Model):
    title = models.CharField(max_length = 400)
    info = models.CharField(max_length = 400)
    desc = models.CharField(max_length = 400)
    urls = models.CharField(max_length = 400)


    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    @classmethod
    def create(cls, title, info, desc, urls, listing):
        listing = cls(title=title, info=info, desc=desc, urls=urls, listing=listing)

    def __str__(self):
        return str(self.title)