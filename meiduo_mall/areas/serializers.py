from rest_framework import serializers

from .models import Area


class AreaSerializer(serializers.ModelSerializer):
    """
    行政区划信息序列化器
    """
    class Meta:
        model = Area
        fields = ['id', 'name']


class SubAreaSerializer(serializers.ModelSerializer):
    """
    子行政区划信息序列化器
    省和市单一序列化器
    """
    # 默认关系属性只输出主键,可以通过指定序列化器来指定输出的格式，嵌套序列
    # 查询上一级的所有子级
    subs = AreaSerializer(many=True, read_only=True)  # 反向查询序列字段中需要用related_name或者子表小写表名_set

    class Meta:
        model = Area
        fields = ['id', 'name', 'subs']
