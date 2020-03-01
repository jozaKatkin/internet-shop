from allauth.account.views import login
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView
from cart.utils import get_cart
from core.forms import AnonymousCheckoutForm, RegisteredCheckoutForm


class RegisteredCheckoutView(TemplateView):
    template_name = 'registered_checkout.html'
    login_required = True

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
        self.clean_session()
        return redirect('success_url', order.pk)

    def get_context_data(self, **kwargs):
        context = super(RegisteredCheckoutView, self).get_context_data(**kwargs)
        context['registered_form'] = self.form
        context['cart'] = self.cart
        return context

    def create_order(self):
        if self.request.user.is_authenticated:
            registered_order = self.form.save(commit=False)
            registered_order.cart = self.cart
            registered_order.user = self.request.user
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

    def dispatch(self, request, *args, **kwargs):
        self.cart = get_cart(self.request)
        if not self.cart:
            return redirect('order_summary_url')

        self.form = AnonymousCheckoutForm(request.POST if self.request.method == 'POST' else None)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not self.form.is_valid():
            print(self.form.errors)
            return self.get(request, *args, **kwargs)
        order = self.create_order()
        self.clean_session()
        return redirect('success_url', order.pk)

    def get_context_data(self, **kwargs):
        context = super(AnonymousCheckoutView, self).get_context_data(**kwargs)
        context['anonymous_form'] = self.form
        context['cart'] = self.cart
        return context

    def create_order(self):
        if self.request.user.is_authenticated:
            return redirect('order_summary_url')
        else:
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

