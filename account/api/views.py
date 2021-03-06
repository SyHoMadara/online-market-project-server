from rest_framework import parsers, renderers
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.compat import coreapi, coreschema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema
from rest_framework.schemas import coreapi as coreapi_schema
from rest_framework.views import APIView

from account.api.serializer import *
from account.models import User
from product.models import Product

OK = status.HTTP_200_OK
BAD_REQUEST = status.HTTP_400_BAD_REQUEST


@api_view()
@permission_classes([AllowAny, ])
def homepage(request):
    return Response([{'response': 'ist work', 'rrr': 'hihi'}, {'nothing': "is nothing"}])


@api_view(['POST', ])
@permission_classes([AllowAny, ])
def register_account_view(request):
    if request.method == 'POST':
        this_status = None
        serialized_data = RegistrationUserSerializer(data=request.data)
        data = {}
        if serialized_data.is_valid():
            user = serialized_data.save()
            data['response'] = 'successfully registered a new user'
            data['token'] = Token.objects.get(user=user).key
            data['email'] = user.email
            this_status = status.HTTP_200_OK
        else:
            data = serialized_data.errors
            this_status = status.HTTP_400_BAD_REQUEST
        return Response(data=data, status=this_status)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
def update_account_view(request):
    user = request.user
    data = {}
    request.data['is_superuser'] = user.is_superuser
    request.data['email'] = user.email
    request.data['date_joined'] = user.date_joined
    if 'password' in request.data:
        password = request.data['password']
        errors = {}
        try:
            password_validation.validate_password(password, user)
        except ValidationError as e:
            errors['password'] = []
            for ex in e:
                errors['password'].append(ex)
            errors['response'] = "Password is invalid"
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        user.password = make_password(password)

    if 'profile_image' in request.data:
        user.profile_image.delete()
    serializer = UserSerializer(user, request.data)
    if serializer.is_valid():
        serializer.save()
        data['response'] = 'update successfully complete'
        return Response(data)
    else:
        data['response'] = 'Update information failed'
        data['errors'] = serializer.errors
        return Response(data, status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
def get_user_view(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
def get_user_by_email(request):
    data = {}
    try:
        user = User.objects.get(email=request.data['email'])
    except User.DoesNotExist:
        data['response'] = "User doesn't exist"
        this_status = status.HTTP_404_NOT_FOUND
        return Response(data=data, status=this_status)

    serializer = UserSerializer(user)
    this_status = status.HTTP_200_OK
    return Response(serializer.data, status=this_status)


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
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({'response': 'Login successful', 'token': token.key, 'email': user.email})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


obtain_auth_token = ObtainAuthToken.as_view()


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
def set_favorite_product(request):
    data = {}
    product_slug = request.data['slug']
    user = request.user
    try:
        product = Product.objects.get(slug=product_slug)
    except Product.DoesNotExist:
        return Response(data={"response": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    try:
        fav = FavoriteProduct.objects.get(user=user, product=product)
        return Response(data={"response": "this product has been add before"}, status=status.HTTP_403_FORBIDDEN)
    except FavoriteProduct.DoesNotExist:
        favorite_product = FavoriteProduct(user=user, product=product)
        favorite_product.save()
        return Response(data={"response": "setting favorite product successful"}, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
def get_all_favorite_products(request):
    user = request.user
    data = [{'response': 'getting all favorite products successful'}]
    for fav in user.favoriteproduct_set.all():
        data.append(FavoriteGetSerializer(fav).data)
    return Response(data=data, status=status.HTTP_200_OK)
