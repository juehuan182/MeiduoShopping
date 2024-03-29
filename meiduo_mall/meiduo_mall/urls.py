"""meiduo_mall URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import TestView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', TestView.as_view(), name='test'),
    path('users/', include('users.urls', namespace='users')),
    path('verifications/', include('verifications.urls', namespace='verifications')),

    path('areas/', include('areas.urls', namespace='areas')),

    path('', include('goods.urls', namespace='goods')),

    # 第三方登录app
    path('oauth/', include('oauth.urls', namespace='oauth')),

    #ckeditor富文本
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
