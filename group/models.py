from django.db import models
from users.models import CustomUser
from django.utils.text import slugify



# class GroupManager(models.Manager):
#     def get_object_or_404(self, slug):
#         group = Group.objects.get(slug)
#         if group:
#             return group
#         else:
#             return 404



class Group(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200)
    # assigns this at the time of the model's creation
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='group_creator', default=0)
    
    slug = models.SlugField(unique=True, default="group_outdated")

    members = models.ManyToManyField(
        CustomUser, 
        through="Membership", 
        #explicitly define which foreign keys to use to avoid undefined behavior if more f.k. are added to Membership
        through_fields=('group', 'person')
        ) 


    # objects = GroupManager()
    
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
# https://simpleisbetterthancomplex.com/series/2017/09/11/a-complete-beginners-guide-to-django-part-2.html 
    # changed names from tutorial (board->group; topic->board)
class Board(models.Model):
    topic = models.CharField(max_length=255)
    description = models.CharField(max_length=1000, default='')
    
    last_updated = models.DateTimeField(auto_now_add=True)

    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    starter = models.ForeignKey(CustomUser, on_delete=models.CASCADE)



    def __str__(self):
        return str(self.topic)




#posts go on boards
class Post(models.Model):
    content = models.TextField(max_length=4000)

    board = models.ForeignKey(Board, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="post_creator")
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name="post_updater")



    def __str__(self):
        return str(self.created_by + self.created_at)