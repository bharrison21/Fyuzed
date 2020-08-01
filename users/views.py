from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView
from django.http import HttpResponse

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.shortcuts import render, redirect, get_object_or_404

#this type of view is called a Class-based view, so it can use form_class, success_url, and template_name
class SignUpView(CreateView):
    #form class defines which form to use
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
    #can create member methods (also can apply method decorators)



class RegisteredUsersList(ListView):
    model = CustomUser
    template_name = 'user_list.html'

#define other views here, they can also be a function-based view
# Example:        # def example_view(request):
#                 #     return render(request, 'home')



# @method_decorator(login_required, name='get_context_data') #<--( this should prob be here but was causing problems )
class ProfileView(DetailView):
    model = CustomUser
    template_name = 'profile.html'
    #handles slug from urls (slug is url path that differs between models, 
    #   so different users have different profile page urls)
    slug_url_kwarg = 'the_slug'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['now'] = timezone.now()
        return context



class ProfileUpdate(UpdateView):
    model = CustomUser
    #fields = ['username',]
    form_class = CustomUserChangeForm
    template_name= "customuser_update_form.html"
    slug_url_kwarg = 'the_slug'
    slug_field = 'slug'

    #the url to go to next: 'profile/{slug}' --- self.object.slug gives updated username as slug
    def get_success_url(self, **kwargs):         
        return reverse_lazy("profile", args=(self.object.slug,))
    

def send_friend_request(request, the_slug):
    if request.method == "POST":
        receiver = get_object_or_404(CustomUser, slug = the_slug)
        sender = request.user
        #if the current user is not already in the receiver's friend request list or friend list
        if (not receiver.friend_requests.filter(slug = sender.slug).exists() and 
        not receiver.friend_list.filter(slug = sender.slug).exists()):
            # not sure exactly why you add to the sender's list but whatever it works this way
            sender.friend_requests.add(receiver,)
        
        #gets previous page url as string or None if they came from a different domain
            # not necessary if you can only send request from view other profile page (complication should be avoided)
        action = request.META.get('HTTP_REFERER')
        if action is not None:
            return redirect(action, the_slug=the_slug)
        else:
            return render(request, 'home.html')


def handle_friend_request(request, the_slug):
    #slug here is requester's slug
    if request.method == "POST":
        user = request.user
        person = get_object_or_404(CustomUser, slug = the_slug)

        decision = request.POST.get('decision')

        # remove requester from friend requests
        user.friend_requests.remove(person)
        person.friend_requests.remove(user)

        if decision == "Accept":
            user.friend_list.add(person)
            person.friend_list.add(user)
        
        return redirect('profile', user.slug)

# should be able 

#should probably add a delete account view

def swap(first, second):
    temp = first
    first = second
    second = temp

def get_friend_suggestions(request):
    # should suggest based:
        #   - on mutual friends (i.e. a friend of multiple friends)
        #   - fellow group members
    
    if request.method == "GET":
        user = request.user
        scores = {}
        
        # +1 pt for each mutual friend
        friends = user.friend_list.all()
        #go through the user's friends
        for friend in friends:
            their_friends = friend.friend_list.all()
            # go through user's friends' friends
            for their_friend in their_friends:
                # don't suggest yourself or people they you are already friends with
                if (their_friend.username != user.username) and (user not in their_friend.friend_list.all()):
                    if their_friend in scores:
                        # if they are already in scores, increase score
                        scores[their_friend] += 1
                    else:
                        # otherwise, add them with a score of 1
                        scores[their_friend] = 1
    
        # +1 pt for each groupmate 
        groups = user.group_set.all()

        for group in groups:
            members = group.members.all()

            for member in members:
                if (member.username != user.username) and (user not in member.friend_list.all()):
                    if member in scores:
                        scores[member] += 1
                    else:
                        scores[member] = 1
        
        #sort by value -- https://stackoverflow.com/questions/52141785/sort-dict-by-values-in-python-3-6 
        sorted_scores = {k: v for k, v in sorted(scores.items(), key=lambda item: item[1], reverse=True)}
        
        return render(request, 'friend_suggestions.html', {'context': sorted_scores})

        # make a dict where each key is a potential suggested friend
        # the value for each key is an integer value representing how good of suggestion that person is
        # example: someone who you have 3 mutual friends with and are in 2 groups with could have 5 points
        #          someone who you only have 1 mutual friend with and no groups could have 1 point
