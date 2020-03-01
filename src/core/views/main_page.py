from django.views.generic import TemplateView, ListView
from core.models import Product


class MainPageView(ListView):
    template_name = 'main_page.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 10
    queryset = Product.objects.all().active()


class PierogiView(TemplateView):
    template_name = 'main_page.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 10
    queryset = Product.objects.filter(category__title='Pierog').active()


class BulkiView(TemplateView):
    template_name = 'main_page.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 10
    queryset = Product.objects.filter(category__title='Bulka').active()




