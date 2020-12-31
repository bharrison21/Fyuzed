from django.db import models
from django.utils.text import slugify
import uuid


# == Both of these models need a slug or pk == 



class Listing(models.Model):
    name = models.CharField(max_length = 400, unique=True, default=uuid.uuid1)
    info = models.CharField(max_length = 400)

    slug = models.SlugField(unique=True, default=uuid.uuid1)


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

    def __str__(self):
        return str(self.title)