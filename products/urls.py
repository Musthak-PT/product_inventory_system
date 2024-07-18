from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
      
    path('products/create_or_update/', views.ProductCreateOrUpdateApiView.as_view(), name='product-create-or-update'),
    path('products/list/', views.ProductListingApiView.as_view(), name='listing-products'),
    path('subvariant/<pk>/add_stock/', views.AddStockView.as_view(), name='add_stock'),
    path('subvariant/<pk>/remove_stock/', views.RemoveStockView.as_view(), name='remove_stock'),
        
]