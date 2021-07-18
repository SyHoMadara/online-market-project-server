import base64

from django.core.files import File
from rest_framework import serializers
from product.models import Product, ProductCategory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = [
            'slug',
        ]


class ProductSerializer(serializers.ModelSerializer):
    base64_image = serializers.SerializerMethodField()

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
        fields = "__all__"

    def get_base64_image(self, obj):
        f = open(obj.image.path, 'rb')
        image = File(f)
        data = base64.b64encode(image.read())
        f.close()
        return data
