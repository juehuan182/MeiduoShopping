import re

from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from .models import User

from verifications.views import EmailCodeView

class UserSerializer(serializers.ModelSerializer):
    """
       用户的序列化器
        allow: "true"
        email: "44@qq.com"
        password: "11111111"
        password2: "11111111"
        email_code: "261800"
        username: "python"
    """
    # 对模型类中没有的字段仅进行反序列化输入
    # write_only:就是用户post过来的数据，后台服务器处理后不会再经过序列化后返回给客户端,我们在使用手机注册的验证码和填写的密码。
    password2 = serializers.CharField(max_length=20, min_length=8, write_only=True)
    email_code = serializers.CharField(max_length=6, min_length=6, write_only=True)
    allow = serializers.CharField(write_only=True)

    token = serializers.CharField(label='登录状态token', read_only=True)  # 增加token字段

    class Meta:
        model = User
        fields =  ("id","username", "email", "password", "password2", "email_code", "allow", "token")
        extra_kwargs = {
             # 对模型类中的字段添加规则
            'password': {
                'write_only': True,
                'max_length': 20,
                'min_length': 8
            },
            'username': {
                'max_length': 20,
                'min_length': 5
            }
        }

    # 进行字段校验
    '''
    单个字段的验证
    1.在序列化器里定义校验字段的钩子方法   validate_字段
    2.获取字段的数据
    3.验证不通过，抛出异常  raise serializers.ValidationError("错误信息描述")
    4.验证通过，直接返回字段数据
    '''
    def validate_email(self, email):
            """
            验证手机好格式
            :param value: 
            :return: 
            """
            if not re.match(r'?P<email>^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email):
                raise serializers.ValidationError("邮箱格式不正确")
            return email

    def validate_allow(self, allow):
            """
            验证是否同意协议
            :param value: 
            :return: 
            """
            if allow != 'true':
                raise serializers.ValidationError("未同意协议")
            
            return allow

    '''
    多个字段的验证
    1.在序列化器定义validate方法
    2.attrs是所有数据组成的字典
    3.不符合抛出异常 raise serializers.ValidationError("校验不通过的说明")
    '''
    def validate(self, attrs):
            """
            验证密码和邮箱验证码
            :param attrs: 
            :return: 
            """
            # 验证密码
            if attrs['password'] != attrs['password2']:
                raise serializers.ValidationError('两次密码不一致')

            # 获取发送的验证码
            real_email_code = EmailCodeView.checkEmailCode(attrs['email']) # 调用类方法
            if real_email_code is None:
                raise serializers.ValidationError('邮箱验证码过期')
            if real_email_code != attrs['email']:
                raise serializers.ValidationError('短信验证码错误')

            return attrs

    '''
    自定义验证器
    使用：在字段添加   validators=[自定义验证器,]

    title = serializers.CharField(max_length=32,validators=[my_validate,])             # 使用自定义验证器

    # 自定义验证器
    def my_validate(value):
        if "xxx" in value:
            raise serializers.ValidationError("该字段包含敏感词!!!")
        else:
            return value

    '''         
    # 自定义验证器 > 单个字段的验证 > 多个字段的验证


    def create(self, validated_data):
        """
        保存用户数据
        :param validated_data: 
        :return: 
        """
        # 1.删除无用数据==> 字典删除，因为要创建对象需要将多余的数据删除
        del validated_data['email_code']  # 这几个只是用来校验的
        del validated_data['password2']
        del validated_data['allow']

        # 保存，使用模型类的管理器方法，create_user可以由Django自动将密码加密，而create还需要先将密码自己加密再给
        user = User.objects.create_user(**validated_data)

        # 补充生成记录登录状态的token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token


        # 将保存数据返回
        return user



