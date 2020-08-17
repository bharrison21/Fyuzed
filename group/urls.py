from django.urls import path
from .views import GroupList, CreateGroup, ViewGroup, ViewBoard, EditBoard
from . import views
from django.views.generic.base import TemplateView

#define paths. 
#       When you are at '<url>/signup/', it will show SignUpView (as_view needed bc its class based)
#       it's name allows it to be refered to as just 'signup' from other parts of the code, like in home.html


urlpatterns = [
    path('grouplist/', GroupList.as_view(), name="grouplist"),
    path('grouphome/', TemplateView.as_view(template_name='groups/groups_home.html'), name="grouphome"),
    
    path('creategroup/', views.create_group, name="creategroup"),
    path('<slug:the_slug>/', ViewGroup.as_view(), name="viewgroup"),
    path('<slug:the_slug>/joingroup', views.join_group, name="joingroup"),
    path('<slug:the_slug>/leavegroup', views.leave_group, name="leavegroup"),
    path('<slug:the_slug>/deletegroup', views.delete_group, name="deletegroup"),

    path('<slug:the_slug>/createboard', views.create_board, name="createboard"),
    path('<slug:the_slug>/viewboard/<int:pk>', ViewBoard.as_view(), name="viewboard"),
    path('<slug:the_slug>/viewboard/<int:pk>/editboard', EditBoard.as_view(), name="editboard"),
    path('<slug:the_slug>/viewboard/<int:pk>/deleteboard', views.delete_board, name="deleteboard"),

    path('<slug:the_slug>/viewboard/<int:board_pk>/createpost', views.create_post, name="createpost"),
    path('<slug:the_slug>/viewboard/<int:board_pk>/deletepost/<int:post_pk>', views.delete_post, name="deletepost"),
]