from django import forms
from .models import Group, Board, Post



class GroupCreationForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name', 'description',)

    # name = forms.CharField(label='Group Name', max_length=100)
    # description = forms.CharField(label='Group Description', max_length=400)



class BoardCreationForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ('topic', 'description',)



class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content',)



class BoardUpdateForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ('topic', 'description', )