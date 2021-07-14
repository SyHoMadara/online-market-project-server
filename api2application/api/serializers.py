from rest_framework import serializers
from ..models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'userpicture',
            'date_joined',
            'is_superuser',
            'is_staff',
            'is_active',
        ]
        model = User
