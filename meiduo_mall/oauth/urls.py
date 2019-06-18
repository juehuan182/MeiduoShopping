from django.urls import path

from .views import QQAuthURLLoginView, QQAuthView

app_name = 'oauth'

urlpatterns = [
    path('qq/authorization/', QQAuthURLLoginView.as_view(), name='qq_authorization'),
    path('qq/user/', QQAuthView.as_view(), name='qq_user'),


    # path('weibo/authorization/', name='weibo_authorization'),

]
