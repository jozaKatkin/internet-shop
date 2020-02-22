from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

from allauth.account.forms import SignupForm
from django import forms


class UserSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name', required=False)
    last_name = forms.CharField(max_length=30, label='Last Name', required=False)
    phone = forms.CharField(max_length=20, required=False)
    address = forms.CharField(max_length=225, required=False)

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data['phone']
        user.address = self.cleaned_data['address']
        user.save()
        return user


# class LoginForm(AuthenticationForm, forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('username', 'password')
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields:
#             self.fields[field].widget.attrs['class'] = 'form-control'
#
#
# class RegistrationForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#     phone = forms.CharField(max_length=48)
#
#     class Meta:
#         model = User
#         fields = ("username",
#                   'password',
#                   'first_name',
#                   'last_name',
#                   'email',
#                   'phone'
#                   )
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields:
#             self.fields[field].widget.attrs['class'] = 'form_control'
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password"])
#         if commit:
#             user.save()
#         return user


# class EditProfileForm(UserChangeForm):
#     template_name = 'edit_profile.html'
#     phone = forms.CharField(max_length=48)
#
#     class Meta:
#         model = User
#         fields = (
#             'email',
#             'first_name',
#             'last_name',
#             'password',
#             'phone'
#         )
