from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

import csv
import weasyprint

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


class ExportToCSV(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        headers = {
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment; filename="products.csv"'
        }
        response = HttpResponse(headers=headers)
        fields_name = ['name', 'description', 'sku', 'image', 'price',
                       'is_active']
        writer = csv.DictWriter(response, fieldnames=fields_name)
        writer.writeheader()
        for product in Product.objects.iterator():
            writer.writerow(
                {
                    'name': product.name,
                    'description': product.description,
                    'image': product.image.name if product.image else
                    'no image',
                    'sku': product.sku,
                    'price': product.price,
                    'is_active': product.is_active
                }
            )
        return response


class ExportToPdf(TemplateView):
    template_name = 'products/pdf.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = {'products': Product.objects.all()}
        headers = {
            'Content-Type': 'application/pdf',
            'Content-Disposition': 'attachment; filename="products.pdf"'
        }
        html = render_to_string(
            template_name=self.template_name,
            context=context
        )
        pdf = weasyprint.HTML(string=html).write_pdf()
        response = HttpResponse(pdf, headers=headers)
        return response
