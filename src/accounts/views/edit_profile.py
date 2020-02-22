# from django.views.generic import FormView
# from accounts.forms import EditProfileForm
# from django.contrib.messages.views import SuccessMessageMixin
#
#
# class EditProfileView(FormView, SuccessMessageMixin):
#     template_name = 'edit_profile.html'
#     form_class = EditProfileForm
#     success_url = 'user_profile'
#     success_message = 'Profile was successfully edited.'
#
#     def form_valid(self, form):
#         return super().form_valid(form)
