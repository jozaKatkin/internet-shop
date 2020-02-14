from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from accounts.forms import *
from django.shortcuts import render, redirect
from django.views.generic import CreateView, RedirectView
from django.urls import reverse, reverse_lazy
from django.contrib import messages


# class CustomSuccessMessageMixin:
#     @property
#     def success_msg(self):
#         return False
#
#     def form_valid(self, form):
#         messages.success(self.request, self.success_msg)
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         return '%s?id=%s' % (self.success_url, self.object.id)


class UserLoginView(LoginView):
    template_name = 'registration/login.html'
    next = '/'
    # success_msg = 'You are successfully logged in.'
    redirect_authenticated_user = True
    redirect_field_name = 'main_page_url'
    authentication_form = LoginForm


class RegistrationView(CreateView):
    model = User
    template_name = 'register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('main_page_url')
    # success_msg = 'You were successfully registered.'

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        aut_user = authenticate(username=username, password=password)
        login(self.request, aut_user)
        return form_valid


class MyProjectLogout(LogoutView):
    next_page = reverse_lazy('main_page_url')
