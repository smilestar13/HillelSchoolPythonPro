from django.views.generic.edit import FormView

from products.forms import ProductModelForm
from products.models import Product


class ProductsView(FormView):
    template_name = 'products/index.html'
    form_class = ProductModelForm
    success_url = '/products/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.iterator()
        return context
