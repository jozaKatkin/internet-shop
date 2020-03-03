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

    def __init__(self, *args, **kwargs):
        initial_arguments = kwargs.get('initial', None)
        updated_initial = {}
        if initial_arguments:
            user = initial_arguments.get('user', None)
            if user:
                updated_initial['phone'] = getattr(user, 'phone', None)
                updated_initial['address'] = getattr(user, 'address', None)
        kwargs.update(initial=updated_initial)
        super(RegisteredCheckoutForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Order
        fields = ['address', 'phone', 'delivery_time', 'comment']





