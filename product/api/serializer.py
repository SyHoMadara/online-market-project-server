from django.contrib.auth import password_validation, authenticate
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.fields import empty

from product.models import Product, ProductCategory
from account.models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'title',
            'cost',
            'description'
        ]


class ProductGetterSerializer(serializers.ModelSerializer):
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
            'title',
            'cost',
            'description',
            'user',
            'category',
            'slug',
        ]
