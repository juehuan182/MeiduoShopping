from rest_framework import generics

from .models import Area
from .serializers import AreaSerializer

class ProvinceView(generics.ListAPIView):
    """
    返回省份数据
    """
    queryset = Area.objects.filter(parent_id=None) # 过滤查询，返回父级为空的数据
    serializer_class = AreaSerializer





