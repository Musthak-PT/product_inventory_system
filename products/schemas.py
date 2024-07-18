from rest_framework import serializers
from products.models import Product

class ProductResponseSchema(serializers.ModelSerializer):
    class Meta:
        model= Product
        fields = '__all__'
        
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas