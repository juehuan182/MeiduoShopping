from .models import SKU

from rest_framework import generics
from rest_framework.filters import OrderingFilter

from drf_haystack.viewsets import HaystackViewSet

from .serializers import SKUSerializer, SKUIndexSerializer

class SKUListView(generics.ListAPIView):
    """
    SKU列表数据
    """
    # 指定序列化器
    serializer_class = SKUSerializer
    # 过滤器，只针对当前查询过滤，所以不在settings.py中配置
    filter_backends = (OrderingFilter,)
    # 排序
    ordering_fields = ('create_time', 'price', 'sales')

    # 默认情况下 DRF generic list view 会返回整个 queryset查询结果，
    # 但通常业务只是需要其中一部分，这种情况下就需要使用 "过滤器" 来限制返回结果集。
    def get_queryset(self):
        """
        获取查询集
        :return:
        """
        # 获取url路径中 正则组起别名提取参数
        category_id = self.kwargs.get('category_id')

        # 查询指定的分类的,上架的商品is_launched=True
        return SKU.objects.filter(category_id=category_id, is_launched=True)


class SKUSerchViewSet(HaystackViewSet):
    """
    SKU搜索
    """
    index_models = [SKU]

    serializer_class = SKUIndexSerializer