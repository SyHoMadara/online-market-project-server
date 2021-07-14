from rest_framework import serializers
from ..models import User


class UserSerializer(serializers.Serializer):
    class Meta:
        modle = 'User'
        fields = ['id', 'email', 'first_name', 'last_name', 'userpicture']
