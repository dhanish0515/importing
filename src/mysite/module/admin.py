from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Product, ProductVariant, PriceVariant, DurationType
from .resources import ProductResource, ProductVariantResource, PriceVariantResource, DurationTypeResources

# Register your models here.


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    list_display = ('name', 'base_price', 'country', 'is_approved')
    search_fields = ('name', 'slug')
    list_filter = ('country',)


@admin.register(ProductVariant)
class ProductVariantAdmin(ImportExportModelAdmin):
    resource_class = ProductVariantResource
    list_display = ('product', 'variant_name', 'original_price', 'variant_price', 'country')
    search_fields = ('product__name', 'variant_name', 'sku_id')
    list_filter = ('country',)


@admin.register(DurationType)
class DurationTypeAdmin(ImportExportModelAdmin):
    resource_class = DurationTypeResources
    list_display = ('name', 'duration_id')
    search_fields = ('name', 'duration_id')


@admin.register(PriceVariant)
class PriceVariantAdmin(ImportExportModelAdmin):
    resource_class = PriceVariantResource
    list_display = ('product_variant', 'duration_type', 'price', 'selling_price')
    search_fields = ('product_variant__product__name', 'product_variant__variant_name')
    list_filter = ('duration_type',)


