from rest_framework import serializers
from .models import Product, Variant, SubVariant

class SubVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubVariant
        fields = ['id', 'name', 'stock']

class VariantSerializer(serializers.ModelSerializer):
    sub_variants = SubVariantSerializer(many=True)

    class Meta:
        model = Variant
        fields = ['id', 'name', 'sub_variants']

class CreateOrUpdateProductSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=False, help_text="This field is required only when updating API")
    variants = VariantSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'ProductID', 'ProductCode', 'ProductName', 'ProductImage', 'CreatedUser', 'IsFavourite', 'Active', 'HSNCode', 'TotalStock', 'variants']

    def create(self, validated_data):
        request = self.context.get('request')
        variants_data = validated_data.pop('variants')
        product = Product.objects.create(**validated_data, CreatedUser=request.user)  # Set CreatedUser here

        for variant_data in variants_data:
            sub_variants_data = variant_data.pop('sub_variants', [])
            variant = Variant.objects.create(product=product, **variant_data)

            for sub_variant_data in sub_variants_data:
                SubVariant.objects.create(variant=variant, **sub_variant_data)

        return product

    def update(self, instance, validated_data):
        variants_data = validated_data.pop('variants', [])

        instance.ProductID = validated_data.get('ProductID', instance.ProductID)
        instance.ProductCode = validated_data.get('ProductCode', instance.ProductCode)
        instance.ProductName = validated_data.get('ProductName', instance.ProductName)
        instance.ProductImage = validated_data.get('ProductImage', instance.ProductImage)
        instance.IsFavourite = validated_data.get('IsFavourite', instance.IsFavourite)
        instance.Active = validated_data.get('Active', instance.Active)
        instance.HSNCode = validated_data.get('HSNCode', instance.HSNCode)
        instance.TotalStock = validated_data.get('TotalStock', instance.TotalStock)
        instance.save()

        # Update or create variants
        for variant_data in variants_data:
            sub_variants_data = variant_data.pop('sub_variants', [])
            variant_id = variant_data.pop('id', None)

            if variant_id:
                variant = Variant.objects.get(id=variant_id, product=instance)
                for attr, value in variant_data.items():
                    setattr(variant, attr, value)
                variant.save()
            else:
                variant = Variant.objects.create(product=instance, **variant_data)

            # Update or create sub-variants
            for sub_variant_data in sub_variants_data:
                sub_variant_id = sub_variant_data.pop('id', None)

                if sub_variant_id:
                    sub_variant = SubVariant.objects.get(id=sub_variant_id, variant=variant)
                    for attr, value in sub_variant_data.items():
                        setattr(sub_variant, attr, value)
                    sub_variant.save()
                else:
                    SubVariant.objects.create(variant=variant, **sub_variant_data)

        return instance

#________________Adding stock(Purchase)_____________________
class SubVariantAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubVariant
        fields = ['stock']
#________________Removing stock(sales)_____________________
class SubVariantRemoveSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubVariant
        fields = ['stock']       
        
        