import uuid

from django.db import models

# Create your models here.
from django_countries.fields import CountryField


class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(max_length=128, unique=True)
    base_price = models.DecimalField(decimal_places=5, max_digits=15, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    country = CountryField(default="IN", help_text="Product origin country")
    is_approved = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = "products"
        ordering = ('name',)

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    variant_name = models.CharField(max_length=128)
    sku_id = models.CharField(max_length=128, blank=True, null=True)
    original_price = models.DecimalField(max_digits=15, decimal_places=2)
    variant_price = models.DecimalField(max_digits=15, decimal_places=2)
    country = CountryField(default="IN")

    class Meta:
        verbose_name = 'Product Variant'
        verbose_name_plural = 'Product Variants'
        ordering = ('product__name', 'variant_name')

    def __str__(self):
        return f'{self.product.name} - {self.variant_name}'


class DurationType(models.Model):
    duration_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        verbose_name = 'Duration Type'
        verbose_name_plural = 'Duration Types'

    def __str__(self):
        return self.name


class PriceVariant(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    duration_type = models.ForeignKey(DurationType, on_delete=models.CASCADE, db_column='duration_id')
    price = models.DecimalField(max_digits=100, decimal_places=2)
    selling_price = models.DecimalField(max_digits=15, decimal_places=2)
    country = CountryField(default="IN")


    class Meta:
        verbose_name = 'Price Variant'
        verbose_name_plural = 'Price Variants'
        ordering = ('product_variant__product__name', 'product_variant__variant_name')

    def __str__(self):
        return f'{self.product_variant.product.name} - {self.product_variant.variant_name} - {self.duration_type}'

