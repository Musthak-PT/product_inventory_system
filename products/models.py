import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from versatileimagefield.fields import VersatileImageField
from django.contrib.auth.models import User

class Product(models.Model):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ProductID       = models.BigIntegerField(unique=True)
    ProductCode     = models.CharField(max_length=255, unique=True)
    ProductName     = models.CharField(max_length=255)
    ProductImage    = VersatileImageField(upload_to="uploads/", blank=True, null=True)
    CreatedDate     = models.DateTimeField(auto_now_add=True)
    UpdatedDate     = models.DateTimeField(blank=True, null=True , auto_now=True)
    CreatedUser     = models.ForeignKey(User, related_name="user_products", on_delete=models.CASCADE, null=True , blank=True)
    IsFavourite     = models.BooleanField(default=False)
    Active          = models.BooleanField(default=True)
    HSNCode         = models.CharField(max_length=255, blank=True, null=True)
    TotalStock      = models.DecimalField(default=0.00, max_digits=20, decimal_places=8, blank=True, null=True)

    class Meta:
        db_table = "products_product"
        verbose_name = _("product")
        verbose_name_plural = _("products")
        unique_together = (("ProductCode", "ProductID"),)
        ordering = ("-CreatedDate", "ProductID")

class Variant(models.Model):
    product   = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    name      = models.CharField(max_length=255)

class SubVariant(models.Model):
    variant   = models.ForeignKey(Variant, related_name='sub_variants', on_delete=models.CASCADE)
    name      = models.CharField(max_length=255)
    stock     = models.DecimalField(default=0.00, max_digits=20, decimal_places=8)
