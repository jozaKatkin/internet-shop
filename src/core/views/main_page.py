from django.views.generic import TemplateView, ListView
from core.models import Product


class MainPageView(ListView):
    template_name = 'main_page.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.filter(is_active=True)
        context['products'] = products
        return context


class PierogiView(TemplateView):
    template_name = 'main_page.html'
    model = Product
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.filter(is_active=True, category__title='Pierog')
        context['products'] = products
        return context


class BulkiView(TemplateView):
    template_name = 'main_page.html'
    model = Product
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.filter(is_active=True, category__title='Bulka')
        context['products'] = products
        return context





