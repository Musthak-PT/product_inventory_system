from django.shortcuts import render
from .models import Product , SubVariant
from .serializers import CreateOrUpdateProductSerializer , SubVariantAddSerializer , SubVariantRemoveSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .schemas import ProductResponseSchema
from rest_framework import filters
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

# Create your views here.

#________________________Create or update products___________________________
class ProductCreateOrUpdateApiView(generics.GenericAPIView):
    serializer_class = CreateOrUpdateProductSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            id = request.data.get('id')
            if id:
                # Update existing product
                instance = get_object_or_404(Product, pk=id)
                serializer = self.serializer_class(instance, data=request.data, context={'request': request})
            else:
                # Create new product
                serializer = self.serializer_class(data=request.data, context={'request': request})

            if serializer.is_valid():
                saved_instance = serializer.save()
                serialized_data = self.serializer_class(saved_instance, context={'request': request}).data
                response_data = {
                    "status_code": status.HTTP_201_CREATED,
                    "message": "Product has been created successfully" if not id else "Product has been updated successfully",
                    "status": True,
                    "data": serialized_data 
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "status": False,
                    "errors": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "status": False,
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
#________________________Listing of all products___________________________
class ProductListingApiView(generics.ListAPIView):
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductResponseSchema
    filter_backends = [filters.SearchFilter]
    search_fields = ['id']

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        instance_id = request.GET.get('id', None)
        
        if instance_id:
            queryset = queryset.filter(pk=instance_id)
        
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True, context={'request': request})
        
        return self.get_paginated_response(serializer.data)

#________________________Adding stocks ___________________________
class AddStockView(generics.UpdateAPIView):
    queryset = SubVariant.objects.all()
    serializer_class = SubVariantAddSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        additional_stock = request.data.get('stock', 0)

        try:
            additional_stock = int(additional_stock)
        except ValueError:
            return Response({'status': 'Invalid stock value'}, status=status.HTTP_400_BAD_REQUEST)

        if additional_stock < 0:
            return Response({'status': 'Stock value must be positive'}, status=status.HTTP_400_BAD_REQUEST)

        instance.stock += additional_stock
        instance.save()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        return Response({'status': 'Stock added', 'new_stock': instance.stock}, status=status.HTTP_200_OK)
    
#________________________ Removing stocks___________________________
class RemoveStockView(generics.UpdateAPIView):
    queryset = SubVariant.objects.all()
    serializer_class = SubVariantRemoveSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        remove_stock = request.data.get('stock', 0)

        if not isinstance(remove_stock, int):
            try:
                remove_stock = int(remove_stock)
            except ValueError:
                return Response({'status': 'Invalid stock value'}, status=status.HTTP_400_BAD_REQUEST)

        if remove_stock <= 0:
            return Response({'status': 'Stock value must be positive'}, status=status.HTTP_400_BAD_REQUEST)

        if instance.stock < remove_stock:
            return Response({'status': 'Not enough stock to remove'}, status=status.HTTP_400_BAD_REQUEST)

        instance.stock -= remove_stock
        instance.save()

        return Response({'status': 'Stock removed', 'new_stock': instance.stock}, status=status.HTTP_200_OK)