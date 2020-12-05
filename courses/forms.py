from django import forms
from . models import Course, Listing



class CourseCreationForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('_title', '_info', '_desc', '_urls')

    _title = forms.CharField(label = "Course Title", max_length = 200)
    _listing = forms.ModelChoiceField(queryset = Listing.objects.all())
    _info = forms.CharField(label='info', max_length = 400) 
    _desc = forms.CharField(label='desc', max_length = 400)
    _urls = forms.CharField(label='urls', max_length = 400)


class ListingCreationForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ('_name', '_info')

    _name = forms.CharField(label = "Listing Name", max_length = 200)
    _info = forms.CharField(label = 'info', max_length = 400) 

