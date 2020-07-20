from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponse

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView

from .models import Group, Membership, Board
from .forms import GroupCreationForm, BoardCreationForm

from users.models import CustomUser
# Create your views here.


class CreateGroup(CreateView):
    form_class = GroupCreationForm
    success_url = reverse_lazy('grouphome')
    template_name = 'create_group.html'

    #assigns creator of the group, so only they can delete it
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(CreateGroup, self).form_valid(form)



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
        # self.request.session.set['cur_group'] = Group.objects.get_object_or_404(Group, slug = slug_field)
        context = super().get_context_data(**kwargs)
        return context



def delete_group(request, the_slug):
    #==== TODO ====
    #   make it so that not just anyone can delete the group (start with creator of the group, expand to admins)
    #   also test to see that it cleans up all its members properly 

    if request.method == "POST":
        # gets the current group based on its slug
        group = Group.objects.get_object_or_404(Group, slug = the_slug)
        if group.created_by == request.user:
            group.delete()
    return render(request, 'groups_home.html')



def join_group(request, the_slug):
    if request.method == "POST":
        # gets the current group based on its slug
        group = Group.objects.get_object_or_404(Group, slug = the_slug)
        # gets the currently logged in user through request
        user = request.user
        # check that user is not already in the group
        if not group.members.filter(slug = user.slug).exists():

            #create new membership object and save it
            membership = Membership(person=user, group=group)
            membership.save()

            #add that member to the group's member list
            group.members.add(user,)
        return render(request, 'groups_home.html')


def leave_group(request, the_slug):
    if request.method == "POST":
        # gets the current group based on its slug
        group = Group.objects.get_object_or_404(Group, slug = the_slug)
        # gets the currently logged in user through request
        user = request.user
        # check that user is not already in the group
        if group.members.filter(slug = user.slug).exists():
            group.members.remove(user,)
            Membership.objects.filter(person = user).delete()
            # delete the membership object that was used as a through field

        return render(request, 'groups_home.html')
        


class CreateBoard(CreateView):
    form_class = BoardCreationForm
    success_url = reverse_lazy('viewgroup')
    template_name = "create_group.html"


    def form_valid(self, form):
        form.instance.starter = self.request.user
        form.instance.group = self.request.POST['group']
      
        
        # self.request.session.get['cur_group']

        return super(CreateBoard, self).form_valid(form)


def create_board(request, the_slug):
    _group = get_object_or_404(Group, slug=the_slug)
    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']

        user = request.user

        board = Board.objects.create(topic = subject, description = message, starter = user, group = _group)
    
    return redirect('viewgroup', the_slug=the_slug)




def delete_board(request, the_slug):
    pass

def create_post(request, the_slug):
    pass

def delete_post(request, the_slug):
    pass



# TODO:
#     - make it possible to create boards & posts
#     - create friends list 
#     - make admins for groups 
#     - make some groups invite-only
#     - Allocating permissions
