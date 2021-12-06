from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView, name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('add/', views.ProductCreateView.as_view(), name='product-add'),
    path('scan/', views.scan_barcode, name='scan-barcode'),
]
