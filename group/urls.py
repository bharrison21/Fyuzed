from django.urls import path
from .views import GroupList, CreateGroup
from django.views.generic.base import TemplateView

#define paths. 
#       When you are at '<url>/signup/', it will show SignUpView (as_view needed bc its class based)
#       it's name allows it to be refered to as just 'signup' from other parts of the code, like in home.html


urlpatterns = [
    path('grouplist/', GroupList.as_view(), name="grouplist"),
    path('grouphome/', TemplateView.as_view(template_name='groups_home.html'), name="grouphome"),
    path('creategroup/', CreateGroup.as_view(), name="creategroup"),
]