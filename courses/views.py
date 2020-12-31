from django.shortcuts import render, get_object_or_404
from . models import Course, Listing
from . forms import CourseCreationForm, ListingCreationForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import ListView, DetailView

from django.utils.text import slugify

# Create your views here.
@login_required
def create_course(request):
    user = request.user
    context = {
            'form': CourseCreationForm,
        }
    if request.method == 'POST':
        _title = request.POST['_title']
        _listing = request.POST['_listing']
        _info = request.POST['_info']
        _desc = request.POST['_desc']
        _urls = request.POST['_urls']

        listing_obj = get_object_or_404(Listing, pk = _listing)
        course = Course.objects.create(title = _title, listing = listing_obj, info = _info, desc = _desc, urls = _urls)

    
    return render(request, 'courses/create_course.html', context)



#This function doesn't work yet, but I gotta get this working
@login_required
def create_listing(request):
    user = request.user
    context = {
            'form': ListingCreationForm,
        }
    if request.method == 'POST':
        _name = request.POST['_name']
        _info = request.POST['_info']

        listing = Listing.objects.create(name = _name, info = _info)

    
    return render(request, 'courses/create_listing.html', context)




class Listings(LoginRequiredMixin, ListView):
    model = Listing
    template_name = "courses/listings.html"



class ViewListing(LoginRequiredMixin, DetailView):
    model = Listing
    template_name = 'courses/view_listing.html'
    #handles slug from urls (slug is url path that differs between models, 
    #   so different groups have different urls)
    slug_url_kwarg = 'the_slug'
    slug_field = 'slug'


    def get_context_data(self, **kwargs):
        # self.request.session.set['cur_group'] = Group.objects.get_object_or_404(Group, slug = slug_field)
        context = super().get_context_data(**kwargs)
        return context