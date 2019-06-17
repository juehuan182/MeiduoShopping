import logging
import random

from django.shortcuts import render
from django_redis import get_redis_connection

from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status

from celery_tasks.email.tasks import task_send_email_code


# Create your views here.

logger = logging.getLogger('django')


class EmailCodeView(APIView):
    """发送邮件验证码"""
    def get(self, request, email):
        """
            发送邮件验证码
            re_path(r"^sms_codes/(?P<email>1[3-9]\d{9})/$", views.SMSCodeView.as_view()),
            :param request:
            :param mobile: 路径传参的手机号
            :return:       
        """
        send_type = request.query_params.dict().get('send_type')
        print(send_type)

        # 1. 创建redis链接
        redis_conn = get_redis_connection(alias='verify_codes')

        # 2.判断60m内是否不允许重复发送短信
        email_flag_key = 'email_flag_key_%s'%email
        email_flag = redis_conn.get(email_flag_key)
        if email_flag:
            return Response({'message':'发送邮件过于频繁'}, status=status.HTTP_400_BAD_REQUEST)

        # 3. 生成验证码
        if send_type == 'register':
            code_len = 6
        elif send_type == 'resetpwd':
            code_len = 6
        else:
            code_len = 4

        email_code = self.random_str(code_len)


        logger.info(email_code)

        email_code_key = 'email_code_key_%s'%email

        # 发送邮件，调用发送邮件接口
        #from celery_tasks.email import send_email
        # 发送验证码给邮箱
        # #  1. 同步发送邮件
        # result = send_email.task_send_email_code(email, 'register')
        # if result:
        #     return Response({'message':'OK'})
        # else:
        #     return Response({'message':'验证码发送失败，请重新发送！'}, status=status.HTTP_400_BAD_REQUEST)
        # 2. 使用celery异步发送邮件，调用delay
        task_send_email_code.delay(email, email_code, send_type)

        print("邮箱验证码:%s" % email_code)       

            # 在此处设置为True会出现bug
        try:
            # 使用redis管道pipeline，优化redis交互，减少通信次数，
            # 创建redis管道对象
            pl = redis_conn.pipeline()
            
            # 将验证码和是否发送标记存储到redis中

            from verifications import constants

            pl.setex(email_flag_key, constants.SEND_CODE_INTERVAL, 1)  # 是否已发送标志
            pl.setex(email_code_key, constants.EMAIL_CODE_REDIS_EXPIRES, email_code.lower())  # 保存验证码
            # 让管道通知redis执行命令
            pl.execute()
        except Exception as e:
            logger.debug("redis 执行出现异常:{}".format(e))
            return Response({'message':'redis 执行出现异常:{}'.format(e)})

        return Response({'message':'OK'})




    @classmethod
    def checkEmailCode(cls, email):   # 通过@classmethod装饰为类方法，用来判断验证码
        """
        验证邮箱验证码
        :param email: 
        :param email_code: 
        :return: 
        """
        # 建立redis链接
        redis_conn = get_redis_connection(alias='verify_codes')
        email_code_key = 'email_code_key_%s'%email

        real_email = redis_conn.get(email_code_key)            
        return real_email.decode()


    # 在python中的random.randint(a,b)用于生成一个指定范围内的整数，生成的随机数n: a <= n <= b
    # 定义一个随机字符串的方法
    def random_str(self, random_length=8):
        active_code = ''
        chars = 'AaBbCcDdEeFfGgHhIiJjKkLlNnMmOoPpQqRrSsTtUuVvWwXxYyZz012346789'
        length = len(chars) - 1

        # 随机生成激活码
        for i in range(0, random_length):  # 需要生成random_length位随机数，循环对应多少次，每次从chars中读取一个字符，拼接成多少位
            # range：左闭右开；randint：左右皆闭;[]：左闭右开
            active_code += chars[random.randint(0, length)]

        return active_code
