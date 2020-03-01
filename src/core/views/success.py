from django.views.generic import DetailView
from core.models import Order


class SuccessView(DetailView):
    template_name = 'success.html'
    model = Order
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context_data = super(SuccessView, self).get_context_data()
        return context_data

