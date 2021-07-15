from rest_framework import serializers
from rest_framework.serializers import empty, ModelSerializer
from ..models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'image',
            'date_joined',
            'is_superuser',
            'is_staff',
            'is_active',
        ]