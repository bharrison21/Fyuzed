from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import NameForm, CustomUserCreationForm
from .managers import CustomUserManager

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'index.html')

def home(request):
    #might need to use sessions, after the user is logged in, to carry over their data to this point
    return render(request, 'home.html')

""" 
def login_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid: 
            return render(request, 'home.html', {'form' : form})
    else :
        form = CustomUserCreationForm()

    return render(request, 'registration/login.html', {'form' : form}) """


def register(request): 
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid: 
            #imported from managers.py
            CustomUserManager().create_user(form.email, form.password1)
            user = authenticate(request, username=form.email, password=form.password1)
            if user is not None: 
                login(request, user)
                return render(request, 'home.html', {'form' : form})
            else:
                return HttpResponse("Invalid login")

    else :
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form' : form})



def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return render(request, 'home.html', {'form': form})
        else:
            form = NameForm()
            return render(request, 'registration/login.html', {'form': form})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()
        return render(request, 'registration/login.html', {'form': form})

    