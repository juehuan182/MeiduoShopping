import json

from django.conf import settings

from urllib.parse import urlencode, parse_qs
import requests
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadData



class OAuthBase(object):
    def __init__(self, client_id=None, client_secret=None, redirect_uri=None, state=None):
        """
         初始化请求参数
        :param client_id:
        :param client_secret:
        :param redirect_url:
        :param state:
        """
        self.client_id = client_id
        self.client_key = client_secret
        self.redirect_uri = redirect_uri
        self.state = state  # 用于保存登录成功后的跳转页面路径

    # 授权请求 请求用户授权Token，获取Authorization code
    def get_auth_url(self, url):
        """
        获取登录链接
        :return:
        """
        data_dict = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'state': self.state
        }

        # urllib.parse.urlencode 方法，将字典里面所有的键值转化为query-string格式（key=value&key=value）,
        # 多个参数用&分离，并且将中文转码
        url = url.format(urlencode(data_dict))
        return url

    # 令牌请求  获取授权过的Access Token，通过Authorization Code获取Access Token
    def get_access_token(self, url):
        data_dict = {
            'client_id': self.client_id,
            'client_secret': self.client_key,
            'redirect_uri': self.redirect_uri
        }

        url = url.format(urlencode(data_dict))
        headers = {'Accept': 'application/json'}  # 设置接受json类型
        resp = requests.post(url, headers=headers, data=data_dict)  # 根据code获取access_token

        if resp.status_code == 200:
            # result = urllib.parse.parse_qs(resp.json())  # 这个函数主要用于分析URL中query组件的参数，返回一个key-value对应的字典格式；
            result = resp.json()

            return result

    # 获取用户资料
    def get_user_info(self, url):
        resp = requests.get(url)
        if resp.status_code == 200:
            info = resp.json()
            return info

    def get_user_some_info(self, url):
        pass


    @staticmethod
    def generate_save_user_token(openid):
        """
        生成保存用户数据的token
        :return:
        """
        # 加密openid
        # serializer = Serializer(秘钥, 有效期秒)
        serializer = Serializer(settings.SECRET_KEY, expires_in=settings.SAVE_APP_USER_TOKEN_EXPIRES)
        # serializer.dumps(数据), 返回bytes类型
        token = serializer.dumps({'openid': openid})
        return token.decode()

    @staticmethod
    def check_save_user_token(token):
        """
        校验保存用户数据的token
        :param token:
        :return:
        """
        # 解密
        serializer = Serializer(settings.SECRET_KEY, expires_in=settings.SAVE_APP_USER_TOKEN_EXPIRES)
        try:
            data = serializer.loads(token)
        except BadData:  # 验证失败，会抛出itsdangerous.BadData异常
            return None
        else:
            return data.get('openid')





class OAuth_QQ(OAuthBase):
    def get_access_token(self, url):  # QQ 获取access token有点区别所以重写此方法

        params = {'client_id': self.client_id,
                  'client_secret': self.client_key,
                  'redirect_uri': self.redirect_uri
                  }

        url = url.format(urlencode(params))
        resp = requests.get(url, params=params)  # 根据code获取access_token

        if resp.status_code == 200:
            result = parse_qs(resp.text)  # 这个函数主要用于分析URL中query组件的参数，返回一个key-value对应的字典格式；
            # print(result)
            # print(result['access_token'])

            return result['access_token']

        raise Exception('qq请求access_token失败')

    # 获取用户OpenID_OAuth2.0
    def get_open_id(self, url):
        resp = requests.get(url)
        if resp.status_code == 200:
            result = resp.text  # callback( {"client_id":"10sss8870","openid":"758F02ffadd4C38Bfff89792C0946CE"} );

            result_str = result[9:-3]  # {"client_id":"10sss8870","openid":"758F02ffadd4C38Bfff89792C0946CE"}

            result_json = json.loads(result_str)  # 将json格式数据转换为字典,JSON反序列化为Python对象
            self.openid = result_json['openid']

            return self.openid

    # 获取用户一些资料
    def get_user_some_info(self, url):
        info = self.get_user_info(url)
        nick_name = info.get('nickname', '')
        avatar_url = info.get('figureurl_qq_2', '')
        sex = info.get('gender', '')  # 性别，m：男、f：女、n：未知
        open_id = self.openid
        signature = info.get('desc', '')

        if sex == '男':
            sex = 'm'
        elif sex == '女':
            sex = 'f'
        else:
            sex = 'n'

        if not signature:
            signature = '无个性签名'

        someInfo = {'nick_name': nick_name,
                    'avatar_url': avatar_url,
                    'open_id': open_id,
                    'sex': sex,
                    'signature': signature
                    }

        return someInfo