import re
from verifications.views import EmailCodeView

from django.db.models import Q
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from users.models import User
from oauth.models import OAuthUser

from .utils import OAuthBase

class OAuthSerializer(serializers.ModelSerializer):
    """第三方账户绑定的序列化器"""
    # 指定模型类中没有的字段
    email_code = serializers.CharField(max_length=6, min_length=6, write_only=True)
    access_token = serializers.CharField(write_only=True)  # 反序列化输入，可能要进行校验之类的。注意这个是我们自己生成的。
    login_type = serializers.CharField(write_only=True)

    token = serializers.CharField(label='登录状态token', read_only=True)  # 定义只输出的token属性
    user_id = serializers.IntegerField(read_only=True)  # 序列化输出

    class Meta:
        model = User
        fields = ('password', 'email', 'username', 'email_code', 'token', 'access_token', 'login_type', 'user_id')
        extra_kwargs = {
            'username': {
                'read_only': True
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }

    def validate_email(self, email):
            """
            验证邮箱格式
            :param value:
            :return:
            """
            if not re.match(r'\w+@\w+.\w+', email):
                raise serializers.ValidationError("邮箱格式不正确")
            return email

    def validate(self, attrs):
        """
        验证access_token
        :param attrs:
        :return:
        """
        # 校验access_token
        access_token = attrs['access_token']
        openid = OAuthBase.check_save_user_token(access_token)
        if not openid:
            raise serializers.ValidationError('无效的access_token')

        attrs['openid'] = openid

        # 校验验证码
        # 获取发送的验证码
        real_email_code = EmailCodeView.checkEmailCode(attrs['email'])  # 调用类方法
        if real_email_code is None:
            raise serializers.ValidationError('邮箱验证码过期')
        if real_email_code != attrs['email_code'].lower():
            raise serializers.ValidationError('短信验证码错误')

        # 校验第三方登录类型
        login_type = attrs['login_type']
        if not login_type:
            raise serializers.ValidationError('登录类型错误')

        # 校验用户名和邮箱是否被注册过

        user = User.objects.filter(Q(username=attrs['email'])|Q(email=attrs['email'])).first()
        if user: # 注册过，则检查密码是否正确
            if not user.check_password(attrs['password']):
                raise serializers.ValidationError('密码错误')

            attrs['user'] = user

        return attrs

    def create(self, validated_data):
        """
        保存用户
        :param validated_data:
        :return:
        """
        # 判断用户
        user = validated_data.get('user')
        if not user:
            # 创建新用户
            email = validated_data.get('email')
            password = validated_data.get('password')

            user = User.objects.create_user(username=email, email=email,  password=password)


        # 用户与第三方账户绑定
        OAuthUser.objects.create(user=user, openid=validated_data.get('openid'), loginType=validated_data.get('login_type'))

        # 签发jwt token
        # 在创建use对象的时候手动生成token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token  # 为user添加token属性才能输出到客户端
        user.user_id = user.id
        return user




