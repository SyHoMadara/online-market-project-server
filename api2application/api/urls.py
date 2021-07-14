from django.urls import re_path
from .views import user_view

from handlers.validators import EMAIL_REGEX

app_name = 'api2application'
urlpatterns = [
    re_path(r'(?P<email>' + EMAIL_REGEX + ')/', user_view, name='user details'),
]
