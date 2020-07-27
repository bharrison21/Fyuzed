from django.shortcuts import render, redirect
from django.views.generic import ListView
from config.settings import AUTH_USER_MODEL
from users.models import CustomUser
from group.models import Group, Board

# class SearchResultsView(ListView):
#     model = CustomUser
#     template_name = 'search/search_page.html'

#     def get_queryset(self): # new
#         query = self.request.GET.get('query')
#         # search_users = self.request.GET.get('users')
#         # search_groups = self.request.GET.get('groups')
#         # search_boards = self.request.GET.get('boards')

#         object_list = CustomUser.objects.filter(username__contains=query)
#         return object_list


def search(request):
    if request.method=="GET":
        radio = request.GET.get('category')

        query = request.GET.get('query')
        context = {
            'query': query,
            'radio': radio,
        }

        #probably want to limit to first 10-50 results for the sake of time
        if radio == 'users':
            results = CustomUser.objects.filter(username__icontains=query)
            context['results'] = results

        elif radio == 'groups':
            results = Group.objects.filter(name__icontains=query)
            context['results'] = results

        elif radio == 'boards':
            results = Board.objects.filter(topic__icontains=query)
            context['results'] = results

        return render(request, 'search/search_page.html', context)


        