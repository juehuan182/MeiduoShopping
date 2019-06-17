# 为celery使用django配置文件进行设置

import os
from celery import Celery

# 设置django环境，celery 运行时需要读取django中的信息
# if not os.getenv('DJANGO_SETTINGS_MODULE'):
#     os.environ['DJANGO_SETTINGS_MODULE'] = 'meiduo_mall.settings.dev

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meiduo_mall.settings.dev') 

# 创建celery应用, 创建一个Celery类的实例对象
app = Celery('meiduo')

#  导入celery配置
app.config_from_object('celery_tasks.config')

# 自动注册celery任务
app.autodiscover_tasks(['celery_tasks.email', ])