from django.contrib import admin
from .models import *


# admin.site.register(User)
# admin.site.register(Product)
# admin.site.register(ProductCategory)
admin.site.register(Picture)
admin.site.register(Pictures)


@admin.register(ProductCategory)
class ProductCategoriesModel(admin.ModelAdmin):
    list_display = ['__str__', 'parent']


@admin.register(Product)
class ProductCategoriesModel(admin.ModelAdmin):
    list_display = ['title', 'cost', 'product_category']

#
# @admin.register(ProductCategory)
# class ProductCategoriesModel(admin.ModelAdmin):
#     list_display = ['__str__', 'parent']
#
#
# @admin.register(ProductCategory)
# class ProductCategoriesModel(admin.ModelAdmin):
#     list_display = ['__str__', 'parent']
#
#
# @admin.register(ProductCategory)
# class ProductCategoriesModel(admin.ModelAdmin):
#     list_display = ['__str__', 'parent']
