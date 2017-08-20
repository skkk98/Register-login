from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login
from django.template.loader import render_to_string
from django import forms
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

# def index(request):
   # all_users = User.objects.all()
  # return render(request, 'login/index.html', {'all_users': all_users})


def Oh(request):
    return HttpResponse("<h1>If you are reading this then Hell yeaaaah! you are logged in!</h1>")
# OKAY BRO NOW EVERYTHING IS GOING TO CHANGE.
# I HOPE YOU KNOW WHAT I AM GOING TO CHANGE
# LET'S DO IT RIGHT AWAY

class RegisterFormView(View):
    form_class = RegistrationForm
    template_name = 'login/register.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            username = form.cleaned_data['username']


            if password==confirm_password:

                user.set_password(password)
                user.save()

                user = authenticate(username=username, password=password)
                return HttpResponseRedirect('/login/login')
            else:
                return HttpResponse('<a><strong>Passwords do not match!</strong></a><br><a href=""><strong>Click Here</strong></a> <a>to try again!</a>')


class LoginFormView(View):
    form_class = LoginForm
    template_names = 'login/loginn.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_names, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:

            login(request, user)
            return HttpResponseRedirect("oh/")
        else:
            return HttpResponse('<a href=""><strong>Click Here</strong></a> <a>to try again!</a> ')


