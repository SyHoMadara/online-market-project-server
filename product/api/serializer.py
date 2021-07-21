import base64

from django.core.files import File
from rest_framework import serializers
from product.models import Product, ProductCategory
from account.models import User;


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = "__all__"


class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    # base64_image = serializers.SerializerMethodField()

    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='email'
    )
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug'
    )

    class Meta:
        model = Product
        fields = [
            'user',
            'category',
            # 'base64_image',
            'slug',
            'title',
            'description',
            'cost',
        ]

    # def get_base64_image(self, obj: Product):
    #     try:
    #         f = open(obj.image.path, 'rb')
    #     except OSError:
    #         return None
    #     image = File(f)
    #     data = base64.b64encode(image.read())
    #     f.close()
    #     return data
