from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    # prepopulated_fields = {'slug': ('username',)}

    #this is what will be displayed when you go to <url>/admin
    list_display = ['username', 'email', 'is_superuser']

admin.site.register(CustomUser, CustomUserAdmin)