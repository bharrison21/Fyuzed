from django.urls import path
from .views import SignUpView, RegisteredUsersList, ProfileView, ProfileUpdate
from . import views

#define paths. 
#       When you are at '<url>/signup/', it will show SignUpView (as_view needed bc its class based)
#       it's name allows it to be refered to as just 'signup' from other parts of the code, like in home.html


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('userlist/', RegisteredUsersList.as_view(), name='userlist'),
    path('profile/<slug:the_slug>/', ProfileView.as_view(), name='profile'),
    path('profile/<slug:the_slug>/edituser', ProfileUpdate.as_view(), name='edituser'),
    #path('profile/<slug:the_slug/logout/', views.logout, name='logout'),
    path('profile/<slug:the_slug>/send_friend_request', views.send_friend_request, name='send_friend_request'),
    path('profile/<slug:the_slug>/handle_friend_request', views.handle_friend_request, name='handle_friend_request'),

    path('friendsuggestions/', views.get_friend_suggestions, name='friendsuggestions')
    
]