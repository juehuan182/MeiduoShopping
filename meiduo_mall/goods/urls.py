from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import SKUListView, SKUSerchViewSet


app_name = 'goods'
urlpatterns = [
    path('categories/<int:category_id>/skus/', SKUListView.as_view(), name=''),
]

router = DefaultRouter()
router.register('skus/search', SKUSerchViewSet, base_name='skus_search')

urlpatterns += router.urls