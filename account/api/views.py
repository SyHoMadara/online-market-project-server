from django.contrib.auth import password_validation
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from rest_framework import parsers, renderers
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.compat import coreapi, coreschema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema
from rest_framework.schemas import coreapi as coreapi_schema
from rest_framework.views import APIView

from account.api.serializer import UserSerializer, RegistrationUserSerializer, AuthTokenSerializer
from ..models import User

OK = status.HTTP_200_OK
BAD_REQUEST = status.HTTP_400_BAD_REQUEST


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
def register_account_view(request):
    if request.method == 'POST':
        serialized_data = RegistrationUserSerializer(data=request.data)
        data = {}
        if serialized_data.is_valid():
            user = serialized_data.save()
            data['response'] = 'successfully registered a new user'
            data['email'] = user.email
            data['fist_name'] = user.first_name
            data['last_name'] = user.last_name
            data['token'] = Token.objects.get(user=user).key
        else:
            data = serialized_data.errors
        return Response(data=data)


@api_view(['PUT', ])
@permission_classes([IsAuthenticated, ])
def update_account_view(request):
    user = request.user
    data = {}
    if 'profile_image' in request.data:
        user.profile_image.delete()
    serializer = UserSerializer(user, request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        data['response'] = 'Update information failed'
        data['errors'] = serializer.errors
        return Response(data, status.HTTP_400_BAD_REQUEST)


class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    if coreapi_schema.is_enabled():
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="username",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Username",
                        description="Valid username for authentication",
                    ),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Password",
                        description="Valid password for authentication",
                    ),
                ),
            ],
            encoding="application/json",
        )

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


obtain_auth_token = ObtainAuthToken.as_view()


# todo
@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
def get_user_view(request, email):
    pass
