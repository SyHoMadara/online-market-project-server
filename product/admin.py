from django.contrib import admin
from product.models import *
from django.utils.translation import gettext, gettext_lazy as _


# admin.site.register(Product)
# admin.site.register(ProductCategory)

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (_('None'), {'fields': ['name', 'parent']}),
        (_('Information'), {'fields': ['id', 'slug']}),
    ]
    readonly_fields = [
        'slug',
        'id',
    ]
    list_display = ['__str__']
    list_filter = ['is_root']
    search_fields = ['parent', 'name']


@admin.register(Product)
class ProductCategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (_('None'), {'fields': ['title', 'user', 'cost', 'description', 'image', 'category']}),
        (_('Information'), {'fields': ['id', 'slug']}),
    ]
    readonly_fields = [
        'slug',
        'id',
    ]
    list_display = ['__str__']
    search_fields = ['title', 'category', 'user',]
