from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from users.models import User


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }


class UserBackend(ModelBackend):
    """
    自定义用户名或用户认证
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        # 使用get需要注意: 如果查询的对象不存在的话，会抛出一个DoesNotExist的异常
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))  # 或查询，注意email是等于username，因为都是从表单username获取的值
            if user.check_password(password):  # 判断密码.使用django的用户模块自带的方法
                return user

        except Exception as e:

            return None


