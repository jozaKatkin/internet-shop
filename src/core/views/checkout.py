from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView
from cart.utils import get_cart
from core.forms import AnonymousCheckoutForm, RegisteredCheckoutForm
from core.models import Order


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
        self.clean_session()
        return redirect('success_url', order.pk)

    # def get_initial(self):
    #     initial = super(RegisteredCheckoutView, self).get_initial()
    #     initial['address'] = self.request.user.address
    #     initial['phone'] = self.request.user.phone
    #     return initial

    # def get_form_kwargs(self):
    #     kwargs = super(RegisteredCheckoutView, self).get_form_kwargs()
    #     kwargs.update({'address': self.request.user.address})
    #     kwargs.update({'phone': self.request.user.phone})
    #     return kwargs

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
            registered_order.email = self.request.user.email
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

