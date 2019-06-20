from django.shortcuts import render
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import User, Address
from .serializers import UserSerializer, UserDetailSerializer, AddressSerializer
# Create your views here.

class CheckUsername(APIView):
    """验证用户名是否重复"""
    def get(self, request, username):
        """
        验证用户名是否重复
        re_path(r"usernames/(?P<username>\w{5,20})/count/",views.CheckUsername.as_view()),
        :param request:
        :param name:
        :return:
        """
        count = User.objects.filter(username=username).count()

        data = {
                'username': username,
                'count': count
        }

        return Response(data)

        
class CheckEmail(APIView):
    """验证邮箱是否存在"""
    def get(self, request, email):
        """
        验证邮箱是否存在
        re_path(r"emails/(?P<email>^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$)/count/",views.CheckEmail.as_view()),
        :param request:
        :param name:
        :return:
        """
        count = User.objects.filter(email=email).count()

        data = {
                'email': email,
                'count': count
        }

        return Response(data)


class UserView(generics.CreateAPIView): # 相当于(CreateModelMixin, GenericAPIView)
    """
        实现用户注册功能
        url(r"^users/$", views.UserRegister.as_view()),
        传入的参数:
            allow: "true"
            email: "13711111111"
            password: "11111111"
            password2: "11111111"
            email_code: "261800"
            username: "python"
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveAPIView):  # RetrieveAPIView 详情视图扩展
    """用户详情"""
    queryset = User.objects.all()   # 获取查询集
    serializer_class = UserDetailSerializer  # 序列化类
    permission_classes = [IsAuthenticated]   # 局部设置权限认证

    def get_object(self):
        """
        重写get_object,不使用pk值返回user
        因为查看某个对象具体详情，默认URL是需要配置类似
            path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
            但是这里我们没有使用Pk
        :return:
        """
        return self.request.user


class AddressViewSet(CreateModelMixin, UpdateModelMixin, GenericViewSet):
    """
    用户地址新增与修改
    """
    # 指定序列化器
    serializer_class = AddressSerializer
    # 指定权限
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        重写方法，制定查询集
        :return:
        """
        return self.request.user.addresses.filter(is_deleted=False)  # 通过用户反向查询用户的地址

    # POST /addresses/
    def create(self, request, *args, **kwargs):
        """
        这里重写主要是判断地址上限，保存用户地址数据
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 检查用户地址数据数目不能超过上限
        count = request.user.addresses.count()
        # count = Address.objects.filter(user=request.user).count()

        if count >= 10: # 判断地址不能超过10个
            return Response({'message': '用户收货地址达到上限'}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

    # delete /addresses/<pk>/
    def destroy(self, request, *args, **kwargs):
        """
        处理删除
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        address = self.get_object()
        # 进行逻辑删除
        address.is_deleted = True
        address.save()

        return Response(status=status.HTTP_204_NO_CONTENT)





