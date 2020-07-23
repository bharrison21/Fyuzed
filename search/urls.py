from django.urls import path
from . import views
from django.views.generic.base import TemplateView

#define paths. 
#       When you are at '<url>/signup/', it will show SignUpView (as_view needed bc its class based)
#       it's name allows it to be refered to as just 'signup' from other parts of the code, like in home.html


urlpatterns = [
    path('', views.search, name="search"),
]