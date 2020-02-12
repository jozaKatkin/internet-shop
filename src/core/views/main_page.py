from django.views.generic import TemplateView
from core.models import Product


class MainPageView(TemplateView):
    template_name = 'main_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pierogi'] = Product.objects.filter(category=1, is_active=True)
        context['bulki'] = Product.objects.filter(category=2, is_active=True)
        return context
