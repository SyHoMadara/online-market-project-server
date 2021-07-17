from rest_framework import serializers
from product.models import Product, ProductCategory


# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = [
#             'title',
#             'cost',
#             'description'
#         ]
#
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='email'
    )
    # category = CategorySerializer(many=False)
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='email'
    )

    class Meta:
        model = Product
        fields = "__all__"

