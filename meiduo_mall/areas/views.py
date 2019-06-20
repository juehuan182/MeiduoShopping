from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from .models import Area
from .serializers import AreaSerializer, SubAreaSerializer

class AreasViewSet(CacheResponseMixin, ReadOnlyModelViewSet): # CacheResponseMixin放在第一位
    """
    使用省市区数据查询
    """

    pagination_class = None  # 禁用分页，商品功能有全局分页

    # 指定查询集
    # queryset = Area.objects.filter(parent_id=None)  # 过滤查询，返回父级为空的数据
    def get_queryset(self):
        if self.action == 'list':
            # 查询所有的省的数据
            return Area.objects.filter(parent_id=None)
        else:
            # 查询指定PK的数据，查询范围是如下指定
            return Area.objects.all()

    # 指定序列化器
    # serializer_class = AreaSerializer
    # 当进行GET,无pk时,查询所有省信息,使用AreaSerializer
    # 当进行GET,pk时,查询指定pk的数据并输出子地区信息,使用SubAreaSerializer
    def get_serializer_class(self):
        if self.action == 'list':  # 在视图集中，我们可以通过action对象属性来获取当前请求视图集时的action动作是哪个。
            return AreaSerializer   # 列表视图使用
        else:
            return SubAreaSerializer    # 详情视图使用


