import urllib

from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.settings import api_settings


from .utils import OAuth_QQ
from .models import OAuthUser
from .serializers import OAuthSerializer


# 当用户在前端登录界面点击QQ登录按钮后向后端发送请求
class QQAuthURLLoginView(APIView):
    """定义第三方登录的视图类"""
    def get(self, request):
        """
        获取第三方登录链接地址
        :param request:
        :return:
        """
        # 通过request.query_params获取查询字符串，next记录从哪里跳转的
        next = request.query_params.get('next')
        if not next:
            next = "/"

        # 获取QQ登录网页地址
        qq_oauth = OAuth_QQ(client_id=settings.QQ_CLIENT_ID,
                            client_secret=settings.QQ_CLIENT_SECRET,
                            redirect_uri=settings.QQ_REDIRECT_URI,
                            state=next)

        # qq_url = 'https://graph.qq.com/oauth2.0/show?which=Login&display=pc&scope=get_user_info&{0}'
        qq_url = 'https://graph.qq.com/oauth2.0/show?which=Login&display=pc&scope=get_user_info&{0}'

        login_url = qq_oauth.get_auth_url(qq_url)  # 返回QQ登录请求地址

        return Response({"login_url": login_url})



class QQAuthView(APIView):
    """验证QQ登录"""
    def get(self, request):
        """
        第三方登录检查
        :param request:
        :return:
        """
        # 1. 获取code值
        code = request.query_params.get('code')

        # 2. 检查参数
        if not code:
            return Response({'message': '缺少code值'}, status=status.HTTP_400_BAD_REQUEST)


        state = request.query_params.get('state')
        if not state:
            state = '/'

        qq = OAuth_QQ(client_id=settings.QQ_CLIENT_ID,
                            client_secret=settings.QQ_CLIENT_SECRET,
                            redirect_uri=settings.QQ_REDIRECT_URI,
                            state=state)

        url = 'https://graph.qq.com/oauth2.0/token?grant_type=authorization_code&code=' + code + '&state=' + state + '&{0}'

        # 3. 通过code获取access_token的值
        access_token = qq.get_access_token(url)[0]
        print(access_token)

        # 4. 使用AccessToken来获取用户的OpenId
        params = {
            'access_token': access_token
        }

        url = 'https://graph.qq.com/oauth2.0/me?{0}'.format(urllib.parse.urlencode(params))

        openid = qq.get_open_id(url)

        # 5. 判断是否绑定过网站账号
        loginType = '1'

        try:
            qq_user = OAuthUser.objects.get(openid=openid, loginType=loginType)

        except OAuthUser.DoesNotExist:
            # 用户第一次使用QQ登录，未绑定，显示绑定界面
            bind_token = OAuth_QQ.generate_save_user_token(openid)

            return Response({'bind_token': bind_token})

        else:
            # 7. 绑定过，则直接登录成功
            # 生成jwt-token值
            user = qq_user.user  # 直接通过外键获取到openid 绑定的用户
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER  # 加载生成载荷函数
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER  # 加载生成token的函数

            payload = jwt_payload_handler(user)  # 通过传入user对象生成jwt 载荷部分
            token = jwt_encode_handler(payload)  # 传入payload 生成token

            dict_data = {
                'user_id': user.id,
                'username': user.username,
                'token': token
            }

            return Response(dict_data)


    def post(self, request):
        """
        QQ绑定页面的请求，完成绑定用户操作
        :param request:
        :return:
        """
        # 1. 获取前端数据
        data = request.data
        # 2. 创建序列化器进行反序列操作
        verified_data = OAuthSerializer(data=data)  # 反序列化传的是data，注意区分
        # 校验数据
        if verified_data.is_valid():
            verified_data.save()
            # print(verified_data.data) # 需要保存之后才能获取.data
            return Response(verified_data.data)

        return Response(verified_data.errors, status=status.HTTP_400_BAD_REQUEST)







