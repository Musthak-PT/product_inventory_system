from django.contrib import admin
from products.models import Product , Variant , SubVariant

# Register your models here.
admin.site.register(Product)
admin.site.register(Variant)
admin.site.register(SubVariant)
