from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView
from django.http import HttpResponse

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render

#this type of view is called a Class-based view, so it can use form_class, success_url, and template_name
class SignUpView(CreateView):
    #form class defines which form to use
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
    #can create member methods (also can apply method decorators)

class RegisteredUsersList(ListView):
    model = CustomUser
    template_name = 'temp.html'

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
    



# def update_profile(request):
#     if request.method == "POST":
#         request.slug_url_kwarg = 'the_slug'
#         request.slug_field = 'slug'
#         user = request.object
#         user.username = request.new_username
#         return render(request, 'profile')