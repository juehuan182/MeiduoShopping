from django.urls import path
from django.urls import re_path

from .views import EmailCodeView

app_name='verifications'
urlpatterns = [
      re_path(r'email_codes/(?P<email>\w+@\w+.\w+)/', EmailCodeView.as_view(), name='email_codes'),
]
