from django.contrib import admin

from .forms import GroupCreationForm, BoardCreationForm, PostCreationForm
from .models import Group, Board, Post

class CustomGroupAdmin(admin.ModelAdmin):
    add_form = GroupCreationForm
    # form = #this needs to be the change form
    model = Group

    # prepopulated_fields = {'slug': ('username',)}

    #this is what will be displayed when you go to <url>/admin
    list_display = ['name', 'description', 'created_at']

admin.site.register(Group, CustomGroupAdmin)