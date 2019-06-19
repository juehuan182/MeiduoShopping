from django.urls import path
from django.urls import re_path

from rest_framework_jwt.views import obtain_jwt_token


from .views import CheckUsername, CheckEmail, UserView, UserDetailView

app_name = 'users'
urlpatterns = [
      re_path(r'usernames/(?P<username>\w{5,20})/count/', CheckUsername.as_view(), name='check_username'),
      re_path(r'emails/(?P<email>\w+@\w+.\w+)/count/', CheckEmail.as_view(), name='check_email'),
      path('', UserView.as_view(), name='users'),
      path('user/detail/', UserDetailView.as_view(), name='user_detail'),

      path('authorizations/', obtain_jwt_token),

]
