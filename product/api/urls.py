from django.urls import re_path
from .views import *

app_name = 'product'
UUID_REGEX = '[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}'

urlpatterns = [
    re_path(r'product/(?P<slug>[0-9a-zA-Z-_]+)/', product_view, name='product api'),
    re_path(r'product/create/', product_view, name='product create api'),
    re_path(r'category/all/',category_view, name='category api'),
    re_path(r'category/(?P<slug>[0-9a-zA-Z-_]+)/',get_product_of_category_view, name='product of category api'),
]