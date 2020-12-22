from django.db import models

# == Both of these models need a slug or pk == 



class Listing(models.Model):
    name = models.CharField(max_length = 400)
    info = models.CharField(max_length = 400)


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