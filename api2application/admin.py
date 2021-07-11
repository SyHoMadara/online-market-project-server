from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(Picture)
admin.site.register(Pictures)