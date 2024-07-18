from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
      
    # path('products/', ProductListView.as_view(), name='product-list'),
    path('products/create/', views.ProductCreateOrUpdateApiView.as_view(), name='product-create-or-update'),
    path('products/list/', views.ProductListingApiView.as_view(), name='listing-products'),
    # path('stock/add/<int:pk>/', AddStockView.as_view(), name='add-stock'),
    # path('stock/remove/<int:pk>/', RemoveStockView.as_view(), name='remove-stock'),
    
]