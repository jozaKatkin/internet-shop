# from django.contrib.auth import authenticate, login
# from django.contrib.auth.views import LoginView, LogoutView
# from django.contrib.messages.views import SuccessMessageMixin
# from accounts.forms import *
# from django.views.generic import CreateView
# from django.urls import reverse, reverse_lazy
#
#
# class UserLoginView(LoginView, SuccessMessageMixin):
#     template_name = 'registration/login.html'
#     next = '/'
#     success_message = 'You are successfully logged in.'
#     redirect_authenticated_user = True
#     redirect_field_name = 'main_page_url'
#     authentication_form = LoginForm
#
#
# class UserRegistrationView(CreateView):
#     model = User
#     template_name = 'register.html'
#     form_class = RegistrationForm
#     success_url = reverse_lazy('main_page_url')
#     success_message = 'You were successfully registered.'
#
#     def form_valid(self, form):
#         form_valid = super().form_valid(form)
#         username = form.cleaned_data["username"]
#         password = form.cleaned_data["password"]
#         firstname = form.cleaned_data["firstname"]
#         lastname = form.cleaned_data["lastname"]
#         email = form.cleaned_data["email"]
#         phone = form.cleaned_data["phone"]
#         aut_user = authenticate(username=username, password=password, firstname=firstname, lastname=lastname,
#                                 email=email, phone=phone)
#         login(self.request, aut_user)
#         return form_valid
#
#
# class UserLogoutView(LogoutView, SuccessMessageMixin):
#     next_page = reverse_lazy('main_page_url')
#     success_message = 'You successfully logged out.'
