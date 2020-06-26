from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView

from .forms import CustomUserCreationForm
from .models import CustomUser

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