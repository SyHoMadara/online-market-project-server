from django.contrib.auth import password_validation
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

from ..models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'profile_image',
            'date_joined',
            'is_superuser',
            'is_staff',
            'is_active',
        ]


class RegistrationUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    password_errors = {}

    def save(self):
        user = User(
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Password mis match'})
        try:
            password_validation.validate_password(password, user)
        except ValidationError as e:
            self.password_errors['password'] = []
            for ex in e:
                self.password_errors['password'].append(ex)
            raise serializers.ValidationError(self.password_errors)
        user.password = make_password(password)
        user.save()
        return user
