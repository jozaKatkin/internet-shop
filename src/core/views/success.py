from django.views.generic import TemplateView
from core.models import Order


class SuccessView(TemplateView):
    template_name = 'success.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = Order.objects.get(user=self.request.user, is_ordered=False)
        order.is_ordered = True
        order.save()
        context['order'] = order
        return context
