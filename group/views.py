from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy

from django.http import HttpResponse

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView

from .models import Group, Membership
from .forms import GroupCreationForm

from users.models import CustomUser
# Create your views here.


class CreateGroup(CreateView):
    form_class = GroupCreationForm
    success_url = reverse_lazy('grouphome')
    template_name = 'create_group.html'



class GroupList(ListView):
    model = Group
    template_name = "group_list.html"



class ViewGroup(DetailView):
    model = Group
    template_name = 'view_group.html'
    #handles slug from urls (slug is url path that differs between models, 
    #   so different groups have different urls)
    slug_url_kwarg = 'the_slug'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def join_group(request, the_slug):
    if request.method == "POST":
    #need to check that user is not already in the group
        user = request.user
        #group = get_object_or_404(Group, slug = the_slug)
        group = Group.objects.get(slug = the_slug)

        #create new membership object and save it
        membership = Membership(person=user, group=group)
        membership.save()

        #add that member to the group's member list
        group.members.add(user,)
        return render(request, 'groups_home.html')




# TODO:
#     - add check so that the same person cannot join the group multiple times
#     - add a choice to leave the group
#     - make it possible to create boards & posts
#     - create friends list 
#     - make owner and admins for groups 
#     - make some groups invite-only
#     - Allocating permissions
