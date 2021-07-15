from rest_framework import parsers, renderers
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.compat import coreapi, coreschema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema
from rest_framework.schemas import coreapi as coreapi_schema
from rest_framework.views import APIView

from account.api.serializer import UserSerializer, RegistrationUserSerializer, AuthTokenSerializer
from ..models import User

OK = status.HTTP_200_OK
BAD_REQUEST = status.HTTP_400_BAD_REQUEST


@api_view(['GET', 'PUT', 'POST'])
def account_view(request, email):
    method = request.method
    if method == 'GET':
        return get_account_view(request, email)
    elif method == 'PUT':
        return update_account_view(request, email)
    # elif method == 'DELETE':
    #     return delete_user_view(request, email)
    elif method == 'POST':
        return register_account_view(request)
    else:
        return Response(status=BAD_REQUEST)


def get_account_view(request, email):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user)
    return Response(serializer.data, status=OK)


# todo fix update account view
def update_account_view(request, email):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    data = {'error': list(), 'success': list()}
    # todo provide update data if password wasn't correct
    # password = request.data['password']
    # if password is None or password != user.password:
    #     data['error'].append('PASSWORD_PROBLEM')
    #     this_status = status.HTTP_403_FORBIDDEN
    #     return Response(data=data, status=this_status)

    serialize = UserSerializer(user, data=request.data)
    if serialize.is_valid():
        data['success'].append('UPDATE_SUCCESS')
        serialize.save()
        this_status = OK
        return Response(data=data, status=this_status)
    else:
        data['error'].append('DATA_NOT_VALID')
        this_status = BAD_REQUEST
    return Response(data=data, status=this_status)


@api_view(['POST', ])
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