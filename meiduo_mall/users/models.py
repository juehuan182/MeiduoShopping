from django.db import models
from django.contrib.auth.models import AbstractUser

from utils.models import BaseModel

# Create your models here.
class User(AbstractUser):
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机')
    # 这里外键关联的是下面定义的，如果不用引号则会陷入循环调用不到的，因为他们2个彼此调用对方，所以用引号可以解决这问题。
    default_address = models.ForeignKey('Address', related_name='users', null=True, blank=True,
                                        on_delete=models.SET_NULL, verbose_name='默认地址')



    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class Address(BaseModel):
    """
    用户地址
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name='用户')
    title = models.CharField(max_length=20, verbose_name='地址名称')
    receiver = models.CharField(max_length=20, verbose_name='收货人')
    province = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='province_addresses', verbose_name='省')
    city = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='city_addresses', verbose_name='市')
    district = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='district_addresses', verbose_name='区')
    place = models.CharField(max_length=50, verbose_name='详细地址')
    mobile = models.CharField(max_length=11, verbose_name='手机')
    tel = models.CharField(max_length=20, null=True, blank=True, default='', verbose_name='固定电话')
    email = models.EmailField(max_length=30, null=True, blank=True, default='', verbose_name='电子邮箱')
    is_deleted = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'tb_address'
        # 默认是按照id排序,可以指定为按照修改时间降序排列
        ordering = ['-update_time']

        verbose_name = '收获地址'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.place
"""
    Address模型类中的外键指向Areas / models里面的Area，指明外键ForeignKey时，可以使用字符串应用名.模型类名来定义
    related_name
    在进行反向关联查询时使用的属性，如
    city = models.ForeignKey(‘areas.Area’, related_name =‘city_addresses’)表示可以通过Area对象.city_addresses属性获取所有相关的city数据。
    ordering
    表名在进行Address查询时，默认使用的排序方式
    models.PROTECT: 保护模式，如果采用该选项，删除的时候，会抛出ProtectedError错误。
"""