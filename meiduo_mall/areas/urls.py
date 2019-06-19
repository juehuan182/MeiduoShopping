from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import AreasViewSet

app_name = 'areas'

# 视图集的路由生成
router = DefaultRouter()
router.register('', AreasViewSet, base_name='areas')

urlpatterns = [

]

urlpatterns += router.urls