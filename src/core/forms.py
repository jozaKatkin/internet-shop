from allauth.account.views import SignupView
from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


PAYMENT_CHOICES = (
    ('1', 'Cash'),
    ('2', 'Card')
)


class UserCheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)
    address = forms.CharField(max_length=128, required=False)
    use_default_address = forms.BooleanField(required=False)
    delivery_time = forms.TimeField(required=False, widget=forms.TimeInput(format='%H:%M'))
    phone = forms.CharField(max_length=20, required=False)
    email = forms.EmailField(required=False)
    commentary = forms.Textarea()

    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)

