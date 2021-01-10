from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponse

from django.views.generic import ListView, DetailView, UpdateView, TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.base import View

from .models import Group, Membership, Board, Post
from .forms import GroupCreationForm, BoardCreationForm, PostCreationForm, BoardUpdateForm

from users.models import CustomUser


from django.utils.text import slugify
# Create your views here.


# THIS CLASS BASED VIEW IS NOT CURRENTLY BEING USED, THE create_group() FUNCTION VIEW IS
class CreateGroup(LoginRequiredMixin, CreateView):
    form_class = GroupCreationForm
    success_url = reverse_lazy('grouphome')
    template_name = 'groups/create_group.html'

    #assigns creator of the group, so only they can delete it
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        #need to add the creator to the members list
        return super(CreateGroup, self).form_valid(form)


class GroupsHome(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        context = {'form': GroupCreationForm}
        return render(request, "groups/groups_home.html", context=context)
    def post(self, request, *args, **kwargs):
        context = {'form': GroupCreationForm}
        create_group(request)
        return render(request, "groups/groups_home.html", context=context)


@login_required
def create_group(request):
    if request.method == "POST":
        _name = request.POST['name']
        _description = request.POST['description']
        user = request.user

        group = Group.objects.create(name = _name, description = _description, created_by = user)
        #add the creator to the group
        join_group(request, group.slug)
    
        return redirect('viewgroup', the_slug = group.slug)
    else:
        return render(request, 'groups/grouphome.html', {'form': GroupCreationForm})



class GroupList(LoginRequiredMixin, ListView):
    model = Group
    template_name = "groups/group_list.html"



class ViewGroup(LoginRequiredMixin, DetailView):
    model = Group
    template_name = 'groups/view_group.html'
    #handles slug from urls (slug is url path that differs between models, 
    #   so different groups have different urls)
    slug_url_kwarg = 'the_slug'
    slug_field = 'slug'


    def get_context_data(self, **kwargs):
        # self.request.session.set['cur_group'] = Group.objects.get_object_or_404(Group, slug = slug_field)
        context = super().get_context_data(**kwargs)
        return context


@login_required
def delete_group(request, the_slug):
    #==== TODO ====
    #   make it so that not just anyone can delete the group (start with creator of the group, expand to admins)
    #   also test to see that it cleans up all its members properly 

    user = request.user 
    if request.method == "POST":
        # gets the current group based on its slug
        group = get_object_or_404(Group, slug = the_slug)
        if group.created_by == user and user in group.members.all():
            group.delete()
            return render(request, 'groups/groups_home.html')
    return redirect('viewgroup', the_slug)


@login_required
def join_group(request, the_slug):
    if request.method == "POST":
        # gets the current group based on its slug
        group = get_object_or_404(Group, slug = the_slug)
        # gets the currently logged in user through request
        user = request.user
        # check that user is not already in the group
        if not group.members.filter(slug = user.slug).exists():

            #create new membership object and save it
            membership = Membership(person=user, group=group)
            membership.save()

            #add that member to the group's member list
            group.members.add(user,)
        return redirect('viewgroup', the_slug)


@login_required
def leave_group(request, the_slug):
    if request.method == "POST":
        # gets the current group based on its slug
        group = get_object_or_404(Group, slug = the_slug)
        # gets the currently logged in user through request
        user = request.user
        # check that user is not already in the group
        if group.members.filter(slug = user.slug).exists():
            group.members.remove(user,)
            Membership.objects.filter(person = user).delete()
            # delete the membership object that was used as a through field

        return redirect('viewgroup', the_slug)


@login_required
def create_board(request, the_slug):
    _group = get_object_or_404(Group, slug = the_slug)

    if request.method == 'POST':
        _topic = request.POST['topic']
        _description = request.POST['description']

        user = request.user
        board = Board.objects.create(topic = _topic, description = _description, starter = user, group = _group)

        return redirect('viewgroup', the_slug = the_slug)
    else:
        context = {
            'group': _group, 
            'slug': the_slug,
            'form': BoardCreationForm,
        }

        return render(request, 'groups/create_board.html', context)
    


class ViewBoard(LoginRequiredMixin, DetailView):
    model = Board
    template_name = 'groups/view_board.html'







class EditBoard(LoginRequiredMixin, UpdateView):
    #TODO: should have check to see if the user is creator / admin
    model = Board
    template_name = 'groups/edit_board.html'

    slug_url_kwarg = 'group_slug'
    slug_field = 'slug'

    pk_url_kwarg = 'pk'
    pk_field = 'int'

    #fields = ['topic', 'description',]
    form_class = BoardUpdateForm

    #the url to go to next: 'profile/{slug}' --- self.object.slug gives updated username as slug
    def get_success_url(self, **kwargs):         
        return reverse_lazy("viewboard", args=(self.object.group.slug, self.object.pk))




@login_required
def delete_board(request, the_slug, pk):
    if request.method == "POST":
        board = get_object_or_404(Board, pk = pk)
        _group = get_object_or_404(Group, slug = the_slug)
        if board.starter == request.user:
            board.delete()
        context = {
            'slug': the_slug,
            'group': _group,
        }
        return render(request, 'groups/view_group.html', context)



@login_required
def create_post(request, the_slug, board_pk):
    _board = get_object_or_404(Board, pk = board_pk)
    _group = get_object_or_404(Group, slug = the_slug)

    if request.method == "POST":
        _content = request.POST['content']
        user = request.user

        post = Post.objects.create(content = _content, board = _board, created_by = user)
    
        return redirect('viewboard', the_slug = the_slug, pk = board_pk)
    else:
        context = {
        'group': _group, 
        'board': _board,
        'form': PostCreationForm,
        }
        return render(request, 'groups/create_post.html', context)



@login_required
def delete_post(request, the_slug, board_pk, post_pk):
    if request.method == "POST":
        post = get_object_or_404(Post, pk = post_pk)
        if post.created_by == request.user:
            post.delete()
    return redirect('viewboard', the_slug=the_slug, pk=board_pk)




# TODO:
#     - make admins for groups 
#     - make some groups invite-only
#     - Allocating permissions
