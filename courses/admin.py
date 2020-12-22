from django.contrib import admin

from .models import Course, Listing


class CustomCourseAdmin(admin.ModelAdmin):
    model = Course

    list_display = ['title', 'listing', 'info', 'desc', 'urls']


class CustomListingAdmin(admin.ModelAdmin):
    model = Listing

    list_display = ['name', 'info']


admin.site.register(Course, CustomCourseAdmin)
admin.site.register(Listing, CustomListingAdmin)
