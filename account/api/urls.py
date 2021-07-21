from django.urls import re_path
from .views import *

app_name = 'account'
urlpatterns = [
    re_path(r'register/', register_account_view, name='register'),
    re_path(r'login/', obtain_auth_token, name='login'),
    re_path(r'update/', update_account_view, name='update'),
    re_path(r'info/', get_user_view, name='information'),
    re_path(r'info-by-email/', get_user_by_email, name='information'),
    re_path(r'set-favorite/', set_favorite_product, name='set favorite product'),
    re_path(r'favorites/', get_all_favorite_products, name='get all favorites'),


    re_path(r'home/page/$', homepage)
]
