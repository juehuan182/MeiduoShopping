import random
import logging

from django.core.mail import send_mail
from django_redis import get_redis_connection
from django.conf import settings

from verifications import constants


# 导入日志器
logger = logging.getLogger('django')


# 定义一个发送邮件
def send_email_code(email, email_code, send_type):


    subject = ''  # 主题
    text_message = ''  # 正文
    html_message = ''  # html格式正文

    if send_type == 'register':
        # print('register')
        subject = u'美多商城-注册验证码'
        text_message = u'【美多商城】您的注册验证码：{0}，请勿将此验证码告知他人，若非本人操作，请联系或者忽略，3分钟内有效！'.format(email_code)  # text格式
        html_message = u'【美多商城】您的注册验证码：{0}，请勿将此验证码告知他人，若非本人操作，请联系或者忽略，3分钟内有效！'.format(email_code)  # html格式方便点击链接

    elif send_type == 'resetpwd':
        subject = u'美多商城-找回密码验证码'
        text_message = u'【美多商城】找回登录密码的验证码：{0}，请勿将此验证码告知他人，若非本人操作，请联系或者忽略，3分钟内有效！'.format(email_code)
        html_message = u'<p>【美多商城】找回登录密码的验证码：{0}，请勿将此验证码告知他人，若非本人操作，请联系或者忽略，3分钟内有效！</p>'.format(email_code)

    elif send_type == 'bindAccount':
        subject = u'美多商城-绑定第三方账号验证码'
        text_message = u'【美多商城】绑定第三方账号的验证码：{0}，请勿将此验证码告知他人，若非本人操作，请联系或者忽略，3分钟内有效！'.format(email_code)
        html_message = u'<p>【美多商城】绑定第三方账号的验证码：{0}，请勿将此验证码告知他人，若非本人操作，请联系或者忽略，3分钟内有效！</p>'.format(email_code)

    else:
        subject = ''
        text_message = ''
        html_message = ''

    # # 保存缓存
    # # mcache.set_key(email, code.lower(), 120)
    # conn_redis = get_redis_connection(alias='verify_codes')

    # # 创建一个在60s以内是否有发送邮件记录的标记
    # email_flag_key = "email_flag_key_{}".format(email).encode('utf-8')

    # # 创建保存邮箱验证码的标记key
    # email_code_key = "email_code_key{}".format(email).encode('utf-8')

    # # 在此处设置为True会出现bug
    # try:
    #     # 使用redis管道pipeline，优化redis交互，减少通信次数，
    #     # 创建redis管道对象
    #     pl = conn_redis.pipeline()

    #     # 将验证码和是否发送标记存储到redis中

    #     pl.setex(email_flag_key, constants.SEND_CODE_INTERVAL, 1)  # 是否已发送标志
    #     pl.setex(email_code_key, constants.EMAIL_CODE_REDIS_EXPIRES, email_code.lower())  # 保存验证码
    #     # 让管道通知redis执行命令
    #     pl.execute()
    # except Exception as e:
    #     logger.debug("redis 执行出现异常:{}".format(e))
    #     return None

    logger.info("email code:{}".format(email_code))
    logger.info("EMAIL_FROM:{}".format(settings.EMAIL_FROM))

    send_status = send_mail(subject, text_message, settings.EMAIL_FROM, [email], html_message)  # 如果提供了html_message，可以发送带HTML代码的邮件。
    print('send_status%s' %send_status)
    return send_status


'''
1.单发send_mail()方法返回值将是成功发送出去的邮件数量（只会是0或1，因为它只能发送一封邮件）。
2.群发 send_mass_mail()，用来处理大批量邮件任务。返回值是成功发送的邮件数量。
使用send_mail()方法时，每调用一次，它会和SMTP服务器建立一次连接，也就是发一次连一次，效率很低。
而send_mass_mail()，则只建立一次链接，就将所有的邮件都发送出去，效率比较高。

需要提醒的是，接收方的邮件服务商不一定支持多媒体邮件，可能为了安全，也许是别的原因。
为了保证邮件内容能被阅读，最好2种格式一起发送纯文本邮件。
'''
