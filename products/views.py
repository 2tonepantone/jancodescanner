from django.views import generic, View
from products.models import Product
from .forms import ProductForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from productscraper.management.commands.crawl import handle_scrape
from scanbarcode import start_scan


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

def scan_barcode(request):
    if request.POST:
        barcode = start_scan()
        if Product.objects.filter(barcode=barcode):
            return handle_redirect(barcode)
        else:
            handle_scrape(barcode)
            return handle_redirect(barcode)
    return HttpResponseRedirect(reverse('index'))

def handle_redirect(barcode):
    product = Product.objects.filter(barcode=barcode)[0]
    return HttpResponseRedirect(f"/products/{product.id}/")
