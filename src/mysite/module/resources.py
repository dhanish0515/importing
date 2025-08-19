import uuid

from import_export import fields, widgets, resources
from import_export.widgets import ForeignKeyWidget
from .models import Product, ProductVariant, PriceVariant, DurationType
from decimal import Decimal, InvalidOperation


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'slug',
            'base_price',
            'description',
            'country',
            'is_approved'
        )
        import_id_fields = ('id',)
        skip_unchanged = True
        report_skipped = True

    def before_import_row(self, row, **kwargs):
        if 'base_price'in row:
            try:
                row['base_price'] = Decimal(str(row['base_price']).replace(',', '').strip())
            except (InvalidOperation, ValueError, ArithmeticError):
                row['base_price'] = None


class ProductVariantResource(resources.ModelResource):
    product = fields.Field(
        column_name='product',
        attribute='product',
        widget=ForeignKeyWidget(Product, 'id')
    )

    class Meta:
        model = ProductVariant
        fields = (
            'id',
            'product',
            'variant_name',
            'original_price',
            'variant_price',
            'sku_id',
            'country',
        )
        import_id_fields = ('id',)

    def before_import_row(self, row, **kwargs):
        decimal_fields = ['original_price', 'variant_price']
        for field in decimal_fields:
            value = row.get(field)
            if value in (None, '', 'N/A', 'null'):
                row[field] = None
            else:
                try:
                    row[field] = Decimal(str(value).replace(',', '').strip())
                except (InvalidOperation, ValueError):
                    row[field] = None


class ProductVariantWidget(widgets.ForeignKeyWidget):
    def clean(self, value=None, row=None, **kwargs):
        #Assuming CSV has both columns:  "variant_name"
        variant_name = (row.get("product_variant") or "").strip() #variant_name coloumn in CSV

        if not variant_name:
            raise Exception(f"Missing product_variant in row: {row}")

        variant = ProductVariant.objects.filter(variant_name=variant_name).first()

        if not variant:
            raise Exception(f"No ProductVariant found for variant_name={variant_name}")

        return variant


class DurationTypeResources(resources.ModelResource):
    class Meta:
        model = DurationType
        fields = ('id', 'name', 'duration_id')


class PriceVariantResource(resources.ModelResource):
    product_variant = fields.Field(
        column_name='product_variant',
        attribute='product_variant',
        widget=ProductVariantWidget(ProductVariant, 'variant_name')
    )

    duration_type = fields.Field(
        column_name='duration_type',
        attribute='duration_type',
        widget=ForeignKeyWidget(DurationType, 'name')
    )

    class Meta:
        model = PriceVariant
        fields = (
            'id',
            'product_variant',
            'duration_type',
            'price',
            'selling_price',
            'country',
        )
        import_id_fields = ('id',)


    def before_import_row(self, row, **kwargs):
        decimal_fields = ['price', 'selling_price']
        for field in decimal_fields:
            value = row.get(field)
            if value in (None, '', 'N/A', 'null'):
                row[field] = None
            else:
                try:
                    row[field] = Decimal(str(value).replace(',', '').strip())
                except (InvalidOperation, ValueError):
                    row[field] = None



