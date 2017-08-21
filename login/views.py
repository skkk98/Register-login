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
from django.conf import settings

# def index(request):
   # all_users = User.objects.all()
  # return render(request, 'login/index.html', {'all_users': all_users})


def Oh(request):
    return HttpResponse("<h1>If you are reading this then Hell yeaaaah! you are logged in!</h1>")


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
                user.is_active = False
                user.set_password(password)
                user.save()
                current_site = get_current_site(request)
                message = render_to_string('login/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                mail_subject = 'Activate your account.'
                to_email = form.cleaned_data.get('email')

                email = EmailMessage(mail_subject, message, settings.EMAIL_HOST_USER, to=[to_email])
                email.send()
                user = authenticate(username=username, password=password)
                return HttpResponse('Please confirm your email address')
            else:
                return HttpResponse('<a><strong>Passwords do not match!</strong></a><br><a href=""><strong>Click Here</strong></a> <a>to try again!</a>')

        return render(request, self.template_name, {'form': form})

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

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Email confirmed. Now you can login')
    else:
        return HttpResponse('Activation link is invalid!')

