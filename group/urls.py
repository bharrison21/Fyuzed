from django.urls import path
from .views import GroupList, CreateGroup, ViewGroup
from . import views
from django.views.generic.base import TemplateView

#define paths. 
#       When you are at '<url>/signup/', it will show SignUpView (as_view needed bc its class based)
#       it's name allows it to be refered to as just 'signup' from other parts of the code, like in home.html


urlpatterns = [
    path('grouplist/', GroupList.as_view(), name="grouplist"),
    path('grouphome/', TemplateView.as_view(template_name='groups_home.html'), name="grouphome"),
    path('creategroup/', CreateGroup.as_view(), name="creategroup"),
    path('viewgroup/<slug:the_slug>/', ViewGroup.as_view(), name="viewgroup"),

    path('viewgroup/<slug:the_slug>/joingroup', views.join_group, name="joingroup"),
    path('viewgroup/<slug:the_slug>/leavegroup', views.leave_group, name="leavegroup"),
    path('viewgroup/<slug:the_slug>/deletegroup', views.delete_group, name="deletegroup"),

    path('viewgroup/<slug:the_slug>/createboard', views.create_board, name="createboard"),


]