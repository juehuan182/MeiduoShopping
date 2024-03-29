import re

from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from .models import User, Address

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

    token = serializers.CharField(label='登录状态token', read_only=True)  # 定义只输出的token属性

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "password2", "email_code", "allow", "token")
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
            验证邮箱格式
            :param value: 
            :return: 
            """
            if not re.match(r'\w+@\w+.\w+', email):
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
            real_email_code = EmailCodeView.checkEmailCode(attrs['email'])  # 调用类方法
            if real_email_code is None:
                raise serializers.ValidationError('邮箱验证码过期')
            if real_email_code != attrs['email_code'].lower():
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
        # 在创建use对象的时候手动生成token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token  # 为user添加token属性才能输出到客户端


        # 将保存数据返回
        return user



class UserDetailSerializer(serializers.Serializer):
    """
    用户详细信息序列化器
    """
    id = serializers.IntegerField(read_only=True) # 用户id，只输出
    username = serializers.CharField(min_length=5, max_length=20, error_messages={'min_length': "用户名不能少于5个字符",
                                                                                  'max_length': "用户名不能大于20个字符",})

    email = serializers.EmailField(read_only=True)



class AddressSerializer(serializers.ModelSerializer):
    """
    收货地址序列化器
    """
    province_id = serializers.IntegerField(label='省ID', required=True, write_only=True)  # write_only 输入用来校验
    city_id = serializers.IntegerField(label='市ID', required=True, write_only=True)
    district_id = serializers.IntegerField(label='区ID', required=True, write_only=True)

    # 序列化输出
    province = serializers.StringRelatedField(read_only=True)  # read_only 用于输出
    city = serializers.StringRelatedField(read_only=True)  # StringRelatedField 字符串形式关系字段
    district = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Address
        exclude = ['user', 'is_deleted', 'create_time', 'update_time']

    def validate_mobile(self, value):
        """
        验证手机号格式
        :param value:
        :return:
        """
        if not re.match(r'1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式错误')

        return value

    def create(self, validated_data):
        """
        重写父类方法
        需要在验证后的数据添加user
        :param validated_data:
        :return:
        """
        # 获取user,把user添加到字典中
        validated_data['user'] = self.context['request'].user

        return Address.objects.create(**validated_data)



class AddressTitleSerializer(serializers.Serializer):
    """
    地址标题
    """
    title = serializers.CharField(max_length=20, label='地址名称', error_messages={'max_length': '标题不能超过20个字符'})

    # 修改
    def update(self, instance, validated_data):  # 通过Serializer来序列化，需要重写create和update方法，这里只是用来修改标题，所以重新更新发发即可。
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        return instance
