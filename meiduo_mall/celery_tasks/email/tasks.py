import logging
from celery_tasks.main import app
from . import send_email


logger = logging.Logger('django')

# 创建任务函数
@app.task(name='send_email_code')
def task_send_email_code(email, email_code, send_type):  
    """
    发送邮件验证码的任务
    :param email:
    :param email_code:
    :return:
    """
    try:
        send_status = send_email.send_email_code(email, email_code, send_type)
    except Exception as e:
        logger.error("发送邮件验证码[异常][ email: %s, message: %s ]" % (email, e))

    else: # 如果try里面的语句可以正常执行，那么就执行else里面的语句（相当于程序没有碰到致命性错误）
        if send_status:  # 成功返回1，不成功返回0或者报错
            logger.info("发送邮件验证码[正常][ email: %s, email_code: %s ]" % (email, email_code))
        else:
            logger.warning("发送邮件验证码[失败][ email: %s ]" % email)


