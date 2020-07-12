from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import ListView
from django.views.generic.edit import CreateView

from .models import Group
from .forms import GroupCreationForm
# Create your views here.


class CreateGroup(CreateView):
    form_class = GroupCreationForm
    success_url = reverse_lazy('grouphome')
    template_name = 'create_group.html'



class GroupList(ListView):
    model = Group
    template_name = "group_list.html"


