from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    #can define custom fields for the model (beyond what AbstractUser comes with)
    pass

    #needed for all models to know what to return by default
    def __str__(self):
        return self.username

        
