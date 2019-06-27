from django.contrib import admin
from . import models

from celery_tasks.html.tasks import generate_static_list_search_html


@admin.register(models.GoodsCategory)
class GoodsCategoryAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        """
        当点击admin编辑界面中的保存按钮时就会来调用此方法
        :param request: 本次保存时的请求对象
        :param obj: 要进行保存或修改的模型对象
        :param form: 本次提示表达
        :param change: 是否有修改 True False
        :return: None
        """
        obj.save()
        generate_static_list_search_html.delay()  # 触发异步任务生成商品列表静态页面


    def delete_model(self, request, obj):
        """
        当点击admin编辑界面中的删除按钮时会调用此方法
        :param request: 删除操作的请求对象
        :param obj: 要被删除的模型对象
        :return: None
        """
        obj.delete()
        generate_static_list_search_html.delay()  # 触发异步任务生成商品列表静态页面


# admin.site.register(models.GoodsCategory)
admin.site.register(models.GoodsChannel)
admin.site.register(models.Goods)
admin.site.register(models.Brand)
admin.site.register(models.GoodsSpecification)
admin.site.register(models.SpecificationOption)
admin.site.register(models.SKU)
admin.site.register(models.SKUSpecification)
admin.site.register(models.SKUImage)

