from django.db import models
from django.urls import reverse
from django.core.validators import MinLengthValidator


class Product(models.Model):
    barcode = models.CharField(max_length=13, validators=[
                               MinLengthValidator(13)])
    name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    ingredients = models.TextField()
    size = models.CharField(max_length=255)
    categories = models.CharField(max_length=255)
    image_link = models.CharField(max_length=255)
    time_created = models.DateTimeField()

    def __str__(self):
        return self.barcode

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.pk})
