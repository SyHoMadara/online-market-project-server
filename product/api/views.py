from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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
    data = {}
    if 'category_slug' in request.data:
        try:
            category = ProductCategory.objects.get(slug=request.data['category_slug'])
        except ProductCategory.DoesNotExist:
            data['response'] = 'category dose not exist'
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

    else:
        category = ProductCategory.objects.get(slug='another')

    if 'image' in request.data:
        image = request.data['image']
        product.image = image
    else:
        data['response'] = 'image most be chosen'
        return Response(data)
    product.category = category
    serialized_data = ProductSerializer(product, data=request.data)

    if serialized_data.is_valid():
        product = serialized_data.save()
        data['response'] = 'successfully created'
        data['title'] = product.title
        data['cost'] = product.cost
        data['description'] = product.description
        data['slug'] = product.slug
        data['category'] = product.category.slug
        data['image'] = product.image.path
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
    user = request.user
    # check for permission
    if user != product.user and not user.is_superuser:
        data['response'] = "You don't have permission on this product"
        return Response(data=data, status=status.HTTP_403_FORBIDDEN)

    if 'category_slug' in request.data:
        try:
            category = ProductCategory.objects.get(slug=request.data['category_slug'])
        except ProductCategory.DoesNotExist:
            data['response'] = 'category dose not exist'
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

    else:
        category = ProductCategory.objects.get(slug='another')

    if 'image' in request.data:
        image = request.data['image']
        product.image = image
    else:
        data['response'] = 'image most be chosen'
        return Response(data)

    product.category = category

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

    user = request.user
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

    serializer = ProductSerializer(instance=product)
    return Response(serializer.data)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
def get_product_of_category_view(request, slug):
    data = {}
    try:
        category = ProductCategory.objects.get(slug=slug)
    except ProductCategory.DoesNotExist:
        data['response'] = 'Category not found'
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    if category.is_root:
        data['response'] = 'Category can not be root'
    else:
        for pro in Product.objects.all():
            if pro.category == category:
                data[pro.slug.__str__()] = ProductSerializer(pro).data
        return Response(data)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
def category_view(request):
    data = {}
    for category in ProductCategory.objects.all():
        serializer = CategorySerializer(category)
        data[category.__str__()] = serializer.data
        data[category.__str__()]['name'] = category.__str__()

    return Response(data)
