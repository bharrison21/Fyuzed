from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

from django import forms

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)
    
    email = forms.EmailField(label="Your email")
    #password = forms.PasswordInput()


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)



class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)