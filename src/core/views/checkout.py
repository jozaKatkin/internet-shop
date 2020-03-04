from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView
from cart.utils import get_cart
from core.forms import AnonymousCheckoutForm, RegisteredCheckoutForm
from core.models import Order
from datetime import datetime


class RegisteredCheckoutView(TemplateView, LoginRequiredMixin):
    template_name = 'registered_checkout.html'
    login_required = True
    form_class = RegisteredCheckoutForm
    model = Order

    def dispatch(self, request, *args, **kwargs):
        self.cart = get_cart(self.request)
        if not self.cart:
            return redirect('order_summary_url')

        self.form = RegisteredCheckoutForm(request.POST if self.request.method == 'POST' else None)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not self.form.is_valid():
            print(self.form.errors)
            return self.get(request, *args, **kwargs)
        order = self.create_order()
        messages.success(request, 'Your order was successfully created.')
        self.clean_session()
        return redirect('success_url', order.pk)

    def get_context_data(self, **kwargs):
        if not datetime.now().replace(hour=8, minute=00) < datetime.now() < datetime.now().replace(hour=22, minute=00):
            time = False
            messages.warning(self.request, 'You can place an order from 8am to 10pm, please wait.')
            context = super(RegisteredCheckoutView, self).get_context_data(**kwargs)
            context['time'] = time
            return context
        else:
            time = True
            context = super(RegisteredCheckoutView, self).get_context_data(**kwargs)
            context['registered_form'] = RegisteredCheckoutForm(
                initial={'user': self.request.user,
                         'phone': self.request.user.phone,
                         'address': self.request.user.address})

            context['cart'] = self.cart
            context['time'] = time
            return context

    def create_order(self):
        if self.request.user.is_authenticated:
            # registered_order = self.form.save(commit=False)
            data = self.form.cleaned_data
            registered_order = Order(
                **data, cart=self.cart,
                user=self.request.user,
                email=self.request.user.email,
                first_name=self.request.user.first_name,
                last_name=self.request.user.last_name,

            )

            registered_order.save()
            registered_order.create_order_items()

            return registered_order
        else:
            return redirect('order_summary_url')

    def clean_session(self):
        try:
            del self.request.session['user_cart']
        except KeyError:
            self.request.session.create()


class AnonymousCheckoutView(TemplateView):
    template_name = 'anonymous_checkout.html'
    form_class = AnonymousCheckoutForm
    model = Order

    def dispatch(self, request, *args, **kwargs):
        self.cart = get_cart(self.request)
        if not self.cart:
            return redirect('order_summary_url')

        self.form = AnonymousCheckoutForm(request.POST if self.request.method == 'POST' else None)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not self.form.is_valid():
            return self.get(request, *args, **kwargs)
        order = self.create_order()
        messages.success(request, 'Your order was successfully created.')
        self.clean_session()
        return redirect('success_url', order.pk)

    def get_context_data(self, **kwargs):
        if not datetime.now().replace(hour=8, minute=00) < datetime.now() < datetime.now().replace(hour=22, minute=00):
            time = False
            messages.warning(self.request, 'You can place an order from 8am to 10pm, please wait.')
            context = super(AnonymousCheckoutView, self).get_context_data(**kwargs)
            context['time'] = time
            return context
        else:
            context = super(AnonymousCheckoutView, self).get_context_data(**kwargs)
            context['anonymous_form'] = self.form
            context['cart'] = self.cart
            time = True
            context['time'] = time
        return context

    def create_order(self):
        anonymous_order = self.form.save(commit=False)
        anonymous_order.cart = self.cart
        anonymous_order.save()
        anonymous_order.create_order_items()
        return anonymous_order

    def clean_session(self):
        try:
            del self.request.session['user_cart']
        except KeyError:
            self.request.session.create()
