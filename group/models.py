from django.db import models
from users.models import CustomUser
from django.utils.text import slugify


class Group(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200)
    # assigns this at the time of the model's creation
    created_at = models.DateTimeField(auto_now=True)
    
    slug = models.SlugField(unique=True, default="group_outdated")

    members = models.ManyToManyField(
        CustomUser, 
        through="Membership", 
        #explicitly define which foreign keys to use to avoid undefined behavior if more f.k. are added
        through_fields=('group', 'person')
        ) 
    
    def save(self, *args, **kwargs):
        #slugify gets rid of spaces, makes it all lowercase, etc.
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


    def __str__(self):
        return str(self.name)




#intermediate model to manage the relationship between users and the members list of a group
#   https://docs.djangoproject.com/en/3.0/topics/db/models/#extra-fields-on-many-to-many-relationships 
class Membership(models.Model):
    person = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField(auto_now=True)
    # invite_reason = models.CharField(max_length=64)



    def __str__(self):
        return str(self.person)









#a discussion board with a topic and which members of the group can add posts to
class Board(models.Model):
    topic = models.CharField(max_length=255)
    description = models.CharField(max_length=1000, default='boardy_mc_boardface')
    
    last_updated = models.DateTimeField(auto_now_add=True)

    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='topics')
    starter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='topics')



    def __str__(self):
        return str(self.topic)




#posts go on boards
class Post(models.Model):
    content = models.TextField(max_length=4000)

    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='posts')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='+')



    def __str__(self):
        return str(self.created_by + self.created_at)