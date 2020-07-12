from django import forms
from .models import Group



class GroupCreationForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name', 'description')
        
    # name = forms.CharField(label='Group Name', max_length=100)
    # description = forms.CharField(label='Group Description', max_length=400)



class BoardCreationForm(forms.Form):
    name = forms.CharField(label='Board Name', max_length=100)



class PostCreationForm(forms.Form):
    content = forms.CharField(label='Board Name', max_length=1000)