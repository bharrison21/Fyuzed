from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import NameForm


def home(request):
    return HttpResponse('Hello, World!')

def login(request):
    return render (request, 'login.html')

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

    