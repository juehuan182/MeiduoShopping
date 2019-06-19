from django.urls import path
from django.urls import re_path

from .views import ProvinceView


app_name = 'areas'
urlpatterns = [
      path('', ProvinceView.as_view(), name='area_province'),
]
