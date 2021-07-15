from django.urls import re_path
from .views import *

from handlers.validators import EMAIL_REGEX

app_name = 'account'
urlpatterns = [
    re_path(r'(?P<email>' + EMAIL_REGEX + ')/', account_view, name='user api'),
    re_path(r'register/', register_account_view, name='register')
]