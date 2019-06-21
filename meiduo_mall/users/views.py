from django.shortcuts import render
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import action

from .models import User, Address
from .serializers import UserSerializer, UserDetailSerializer, AddressSerializer, AddressTitleSerializer
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


class UserView(generics.CreateAPIView):     # 相当于(CreateModelMixin, GenericAPIView)
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


class AddressViewSet(CreateModelMixin, UpdateModelMixin, ListModelMixin, GenericViewSet):
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

    # POST /users/addresses/
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
        if count >= 10:  # 判断地址不能超过10个
            return Response({'message': '用户收货地址达到上限'}, status=status.HTTP_400_BAD_REQUEST)
        # # 创建序列化器进行反序列化
        # serializer = self.get_serializer(data=request.data, context={})
        # # 调用序列化器校验方法
        # serializer.is_valid(raise_exceptions=True)
        # # 调用序列化器的save()
        # serializer.save()
        # # 响应
        # return Response(serializer.data, status=status.HTTP_201_CREATED)

        return super().create(request, *args, **kwargs)


    # delete /users/addresses/<pk>/
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

    # # GET /users/addresses/
    def list(self, request, *args, **kwargs):
        """
        用户地址列表数据，重写list方法
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        user = request.user

        # print(serializer.data)

        return Response({
            'user_id': user.id,
            'default_address_id': user.default_address_id,
            'limit': 10,
            'addresses': serializer.data
        })




    # 视图集中包含附加action的，什么是附加比如不是list,create, destroy,update自带的方法
    # put /users/addresses/pk/status/--->地址是使用DefaultRouter生成的
    @action(methods=['put'], detail=True)  # methods指定请求方式,detail指定是否接收pk
    def status(self, request, pk=None):
        """
        设置默认地址
        :param request:
        :param pk:
        :return:
        """
        address = self.get_object()  # 根据PK获取当前地址对象
        request.user.default_address = address
        request.user.save()

        return Response({'message': 'OK'}, status=status.HTTP_200_OK)

    # put /users/addresses/pk/title/
    # 需要请求体参数title
    @action(methods=['put'], detail=True)
    def title(self, request, pk=None):
        """
        修改标题
        :param request:
        :param pk:
        :return:
        """
        address = self.get_object()
        verified_data = AddressTitleSerializer(instance=address, data=request.data)
        # raise_exception=True这个参数的意思还是，如果验证错误直接抛异常，不进入下面了。drf捕捉到就会抛出400异常
        verified_data.is_valid(raise_exception=True)
        verified_data.save()
        return Response(verified_data.data)







