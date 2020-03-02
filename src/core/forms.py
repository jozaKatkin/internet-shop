from django import forms
from core.models import Order

# PAYMENT_CHOICES = (
#     ('1', 'Cash'),
#     ('2', 'Card')
# )


class AnonymousCheckoutForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, label='First Name', required=False)
    email = forms.EmailField(required=False)
    last_name = forms.CharField(max_length=30, label='Last Name', required=False)
    phone = forms.CharField(max_length=20, required=True)
    address = forms.CharField(max_length=225, required=True)
    comment = forms.CharField(max_length=225, required=False)
    delivery_time = forms.TimeField(required=False)

    class Meta:
        model = Order
        fields = ['address', 'phone', 'delivery_time', 'first_name', 'last_name', 'comment', 'email']


class RegisteredCheckoutForm(forms.ModelForm):
    phone = forms.CharField(max_length=20, required=True)
    address = forms.CharField(max_length=225, required=True)
    comment = forms.CharField(max_length=225, required=False)
    delivery_time = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'class': 'timepicker'}),
                                    input_formats=['%H:%M'])

    class Meta:
        model = Order
        fields = ['address', 'phone', 'delivery_time', 'comment']





