import logging
import os
from celery_tasks.main import app

from goods.utils import get_categories

from django.template import loader
from django.conf import settings

logger = logging.Logger('django')

# 创建任务函数
@app.task(name='generate_static_list_search_html')
def generate_static_list_search_html():
    """
    生成静态的商品列表页和搜索结果页html文件
    :return:
    """
    # 商品分类菜单
    categories = get_categories()

    # 渲染模板,生成静态文件
    context = {
        'categories':categories
    }

    template = loader.get_template('static_list.html')
    static_list_html = template.render(context)
    file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'list.html')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(static_list_html)

