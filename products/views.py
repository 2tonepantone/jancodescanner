from django.views import generic, View
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from productscraper.management.commands.crawl import handle_scrape
from products.models import Product
from .forms import ProductForm
from scanbarcode import extract_barcode
import json


def IndexView(request):
    form = ProductForm()
    template_name = 'products/index.html'

    products = Product.objects.order_by('-time_created')
    return render(request, 'products/index.html', {'form': form,
                                                   'products': products,
                                                   'template_name': template_name})


class DetailView(generic.DetailView):
    model = Product
    template_name = "products/detail.html"


class ProductCreateView(View):
    template_name = 'products/index.html'
    form_class = ProductForm
    products = Product.objects.order_by('-time_created')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            barcode = form.cleaned_data['barcode']
            if Product.objects.filter(barcode=barcode):
                return handle_redirect(barcode)
            else:
                handle_scrape(barcode)
                return handle_redirect(barcode)
        else:
            return render(request, self.template_name, {'form': form,
                                                        'products': self.products})

@csrf_exempt
def scan_barcode(request):
    dataURL = json.loads(request.body.decode('utf-8'))['dataURL']
    barcode = extract_barcode(dataURL)
    print("DataURL:", dataURL)
    print("Barcode:", barcode)
    if len(barcode) == 13:
        print('barcode passed')
        if Product.objects.filter(barcode=barcode):
            return handle_redirect(barcode)
        else:
            handle_scrape(barcode)
            return handle_redirect(barcode)
    else:
        print('Failed to find/scrape product')
        return HttpResponseRedirect(reverse('index'))

def handle_redirect(barcode):
    product = Product.objects.filter(barcode=barcode)[0]
    return HttpResponseRedirect(f"/products/{product.id}/")
