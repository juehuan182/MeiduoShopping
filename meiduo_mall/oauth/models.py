from django.db import models

from utils.models import BaseModel

class OAuthUser(BaseModel):
    """
        第三方登录基本模型
    """
    TYPE_CHOICES = (('1', 'qq'), ('2', 'weibo'), ('3', 'github'))
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='用户')
    openid = models.CharField(max_length=64, verbose_name='用户标识openid', db_index=True)
    loginType = models.CharField(max_length=1, choices=TYPE_CHOICES)

    class Meta:
        db_table = 'tb_oauth_user'
        verbose_name = '第三方用户登录'
        verbose_name_plural = verbose_name

