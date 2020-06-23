from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import NameForm, CustomUserCreationForm
from .managers import CustomUserManager


def home(request):
    return HttpResponse("Alright alright alright")

def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid: 
            return render(request, 'home.html', {'form' : form})
    else :
        form = CustomUserCreationForm()

    return render(request, 'login.html', {'form' : form})



def register(request): 
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid: 
            #nice
            CUM = CustomUserManager()
            CUM.create_user(form.email, form.password1)
            return render(request, 'home.html', {'form' : form})
    else :
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form' : form})




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
            return render(request, 'login.html', {'form': form})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()
        return render(request, 'login.html', {'form': form})

    