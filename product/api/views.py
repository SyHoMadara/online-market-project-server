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

from product.api.serializer import *


@api_view(['PUT', 'DELETE', 'GET', 'POST'])
@permission_classes([IsAuthenticated, ])
def product_view(request, slug=None):
    method = request.method
    if method == 'PUT':
        return update_product_view(request, slug)
    elif method == 'DELETE':
        return delete_product_view(request, slug)
    elif method == 'GET':
        return get_product_view(request, slug)
    elif method == 'POST':
        return creat_product_view(request)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


def creat_product_view(request):

    user = request.user
    product = Product(user=user)
    serialized_data = ProductSerializer(product, data=request.data)
    data = {}
    if serialized_data.is_valid():
        product = serialized_data.save()
        data['response'] = 'successfully created'
        data['title'] = product.title
        data['cost'] = product.cost
        data['description'] = product.description
        data['slug'] = product.slug
    else:
        data = serialized_data.errors
    return Response(data=data)


def update_product_view(request, slug):
    global product
    data = {}
    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        data['response'] = 'product not found'
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    user = request.uesr
    # check for permission
    if user != product.user:
        data['response'] = "You don't have permission on this product"
        return Response(data=data, status=status.HTTP_403_FORBIDDEN)

    serialized_data = ProductSerializer(product, data=request.data)
    if serialized_data.is_valid():
        serialized_data.save()
        data['response'] = 'update successfully complete'
        return Response(data=data, status=status.HTTP_200_OK)
    return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)


def delete_product_view(request, slug):
    global product

    data = {}
    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        data['response'] = 'product not found'
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    user = request.uesr
    # check for permission
    if user != product.user:
        data['response'] = "You don't have permission on this product"
        return Response(data=data, status=status.HTTP_403_FORBIDDEN)
    operation = product.delete()
    if operation:
        data['response'] = 'Delete successfully complete'
    else:
        data['response'] = 'Delete filed. Try again'
    return Response(data=data)


def get_product_view(request, slug):
    global product
    data = {}
    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        data['response'] = 'product not found'
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductGetterSerializer(instance=product)
    return Response(serializer.data)


# todo
@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
def get_image_view(request, slug):
    # todo make difference between profile and product image
    pass


# todo
@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
def category_view():
    pass

