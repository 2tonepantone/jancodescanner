from django.views import generic, View
from products.models import Product
from .forms import ProductForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from productscraper.management.commands.crawl import handle_scrape
from scanbarcode import *


class IndexView(generic.ListView):
    template_name = 'products/index.html'
    context_object_name = 'latest_product_list'

    def get_queryset(self):
        """
        Return the last 10 created products.
        """
        return Product.objects.order_by('-time_created')[:10]


class DetailView(generic.DetailView):
    model = Product
    template_name = "products/detail.html"


class ProductCreateView(View):
    template_name = 'products/product_form.html'
    form_class = ProductForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            barcode = form.cleaned_data['barcode']
            handle_scrape(barcode)
            return HttpResponseRedirect(reverse('index'))

        else:
            return render(request, self.template_name, {'form': form})

def scan_barcode(request):
    main()
    return HttpResponseRedirect(reverse('index'))
