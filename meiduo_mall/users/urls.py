from django.urls import path
from django.urls import re_path

from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import routers


from .views import CheckUsername, CheckEmail, UserView, UserDetailView, AddressViewSet

app_name = 'users'
urlpatterns = [
      re_path(r'usernames/(?P<username>\w{5,20})/count/', CheckUsername.as_view(), name='check_username'),
      re_path(r'emails/(?P<email>\w+@\w+.\w+)/count/', CheckEmail.as_view(), name='check_email'),
      path('', UserView.as_view(), name='users'),
      path('user/detail/', UserDetailView.as_view(), name='user_detail'),

      path('authorizations/', obtain_jwt_token),

]

routers = routers.DefaultRouter()
routers.register(r'addresses', AddressViewSet, base_name='addresses')
urlpatterns += routers.urls

# POST /users/addresses/ 新建 -> create
# PUT /users/addresses/<pk>/ 修改 -> update
# GET /users/addresses/ 查询 -> list
# DELETE /users/addresses/  删除 -> destroy

# PUT /users/addresses/<pk>/status/ 设置默认地址  -> status
# PUT /users/addresses/<pk>/title/ 设置标题  -> title

