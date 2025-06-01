from django.shortcuts import render
from django.views.generic import View


class HomePage(View):
    _template_name = 'pages/homepage.html'

    def get(self, request):
        return render(request, self._template_name)