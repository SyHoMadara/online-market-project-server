from django.urls import re_path
from .views import api_details_user_view

app_name = 'api2application'
urlpatterns = [
    re_path(r'(?P<id>\d+)/', api_details_user_view, name='details')
]
