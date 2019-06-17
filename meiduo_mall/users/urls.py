from django.urls import path
from django.urls import re_path

from .views import CheckUsername, CheckEmail, UserView

app_name='users'
urlpatterns = [
      re_path(r'usernames/(?P<username>\w{5,20})/count/', CheckUsername.as_view(), name='check_username'),
      re_path(r'emails/(?P<email>\w+@\w+.\w+)/count/', CheckEmail.as_view(), name='check_email'),
      path('',UserView.as_view(), name='users'),
]
