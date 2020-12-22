from django.urls import path
#from .views import 
from . import views
from .views import Listings, ViewListing
from django.views.generic.base import TemplateView

#define paths. 
#       When you are at '<url>/signup/', it will show SignUpView (as_view needed bc its class based)
#       it's name allows it to be refered to as just 'signup' from other parts of the code, like in home.html


urlpatterns = [
    path('courses_home/', TemplateView.as_view(template_name='courses/courses_home.html'), name="courses_home"),
    path('create_course/', views.create_course, name="create_course"),
    path('create_listing/', views.create_listing, name="create_listing"),
    path('listings/', Listings.as_view(), name="listings"),
    path('view_listing/', ViewListing.as_view(), name="view_listing")

]