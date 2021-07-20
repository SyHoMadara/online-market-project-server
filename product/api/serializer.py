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
    base64_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"

    def get_user(self, obj: User):
        data = {}
        data['first_name'] = obj.first_name
        data['last_name'] = obj.last_name
        data['phone_number'] = obj.phone_number
        data['email'] = obj.email
        return data

    def get_category(self, obj: ProductCategory):
        data = {}
        data['slug'] = obj.slug
        data['name'] = obj.name
        data['full_name'] = obj.__str__()
        return data

    def get_base64_image(self, obj):
        try:
            f = open(obj.image.path, 'rb')
        except OSError:
            return None
        image = File(f)
        data = base64.b64encode(image.read())
        f.close()
        return data
