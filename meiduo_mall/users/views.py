from django.shortcuts import render
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView


from .models import User
from .serializers import UserSerializer
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


class UserView(CreateAPIView): # 相当于(CreateModelMixin, GenericAPIView)
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

