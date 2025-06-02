from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from web.users.forms.registration import UserRegisterForm


class RegistrationView(View):
    _template_name = "pages/auth/registration.html"
    context = {
        'title': 'Регистрация пользователя',
        'form': UserRegisterForm
    }

    def get(self, request):
        context = self.context
        return render(request, self._template_name, context)

    def post(self, request):
        context = self.context
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('homepage')

        context.update({'form': form})
        return render(request, self._template_name, context)