from django.shortcuts import render
from django.views.generic import View


class ViewTest(View):
    _template_name = 'templates/test_page.html'

    def get(self, request):
        return render(self._template_name, 'test_page.html')