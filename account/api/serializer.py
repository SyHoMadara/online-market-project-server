import base64

from django.contrib.auth import password_validation, authenticate
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.files import File
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from ..models import User


class UserSerializer(serializers.ModelSerializer):
    base64_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'profile_image',
            'phone_number',
            'date_joined',
            'base64_image',
        ]

    def get_base64_image(self, obj):
        f = open(obj.image.path, 'rb')
        image = File(f)
        data = base64.b64encode(image.read())
        f.close()
        return data


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


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label=_("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
