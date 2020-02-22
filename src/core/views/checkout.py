from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.views import View
from core.forms import AnonymousCheckoutForm, RegisteredUserCheckoutForm
from core.models import Order
from accounts.models import UserProfile


class RegisteredUserCheckoutView(View):
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            try:
                order = Order.objects.get(user=self.request.user, is_ordered=False)
                user_profile = UserProfile.objects.get(user=self.request.user)
                form = RegisteredUserCheckoutForm()
                context = {
                    'form': form,
                    'order': order,
                }
                if user_profile.address:
                    context.update(
                        {'default_delivery_address': user_profile.address})

                return render(self.request, "checkout.html", context)

            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("checkout_url")

        else:
            return redirect('registered_user_checkout_url')

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            form = RegisteredUserCheckoutForm(self.request.POST or None)
            try:
                order = Order.objects.get(user=self.request.user, is_ordered=False)
                user_profile = UserProfile.objects.get(user=self.request.user)
                if form.is_valid():
                    use_default_address = form.cleaned_data.get(
                        'use_default_address')
                    if use_default_address:
                        print("Using the default address")
                        if user_profile.address:
                            order.address = user_profile.address
                            order.save()
                        else:
                            messages.info(
                                self.request, "No default address available")
                            return redirect('checkout_url')
                    else:
                        print("User is entering a new delivery address")
                        if form.is_valid():
                            order.address = form.cleaned_data.get('address')
                            order.save()
                        else:
                            messages.info(
                                self.request, "Please fill in the required delivery address")

                    order.delivery_time = form.cleaned_data.get('delivery_time')
                    order.save()

                    payment_option = form.cleaned_data.get('payment_option')

                    if payment_option == '1':
                        return redirect('success_url')
                    elif payment_option == '2':
                        return redirect('success_url')
                    else:
                        messages.warning(
                            self.request, "Invalid payment option selected")
                        return redirect('checkout_url')

                else:
                    messages.info(
                        self.request, "Invalid input")
                    context = {'errors': form.errors}
                    return context
            except ObjectDoesNotExist:
                messages.warning(self.request, "You do not have an active order")
                return redirect("order_summary_url")

        else:
            return redirect('registered_user_checkout_url')