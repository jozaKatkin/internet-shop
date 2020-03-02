from django import forms
from .models import UserProfile


class UserSignupForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, label='First Name', required=False)
    last_name = forms.CharField(max_length=30, label='Last Name', required=False)
    phone = forms.CharField(max_length=20, required=False)
    address = forms.CharField(max_length=225, required=False)

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'phone', 'address']

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data['phone']
        user.address = self.cleaned_data['address']
        user.save()
        return user


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
