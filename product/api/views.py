from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from account.api.serializer import *

from product.api.serializer import *


@api_view(['PUT', 'DELETE', 'GET', 'POST'])
@permission_classes([IsAuthenticated, ])
def product_view(request, slug=None):
    method = request.method
    if method == 'PUT':
        return update_product_view(request)
    elif method == 'DELETE':
        return delete_product_view(request)
    elif method == 'GET':
        return get_product_view(request)
    elif method == 'POST':
        return creat_product_view(request)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


def creat_product_view(request):
    user = request.user
    this_status = None
    request.data['user'] = user
    data = {}
    if 'category_slug' in request.data:
        try:
            category = ProductCategory.objects.get(slug=request.data['category_slug'])
        except ProductCategory.DoesNotExist:
            data['response'] = 'category dose not exist'
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

    else:
        category = ProductCategory.objects.get(slug='another')

    # if 'base64_image' in request.data:
    #     image = request.data['base64_image']
    #     product.image =
    request.data['category'] = category
    serialized_data = CreateProductSerializer(data=request.data)

    if serialized_data.is_valid():
        product = serialized_data.save()
        data['response'] = 'successfully created'
        data['title'] = product.title
        data['cost'] = product.cost
        data['description'] = product.description
        data['slug'] = product.slug
        data['category'] = product.category.slug
        this_status = status.HTTP_200_OK
        # data['image'] = product.image.path
    else:
        this_status = status.HTTP_400_BAD_REQUEST
        data = serialized_data.errors
    return Response(data=data, status=this_status)


def update_product_view(request):
    global product
    data = {}
    slug = request['slug']
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


def delete_product_view(request):
    global product
    data = {}
    slug = request['slug']
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


def get_product_view(request):
    global product
    slug = request['slug']
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
    data = [{'response': ""}]
    try:
        category = ProductCategory.objects.get(slug=slug)
    except ProductCategory.DoesNotExist:
        data[0]['response'] = 'Category not found'
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    if category.is_root:
        data[0]['response'] = 'Category can not be root'
    else:
        for pro in Product.objects.all():
            if pro.category == category:
                data += [ProductSerializer(pro).data]
        return Response(data)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
def category_view(request):
    data = []
    i = 0
    for category in ProductCategory.objects.all():
        serializer = CategorySerializer(category)
        data += [serializer.data]
        data[i]['name'] = category.__str__()
        i += 1

    return Response(data)
