from haystack import indexes
from .models import SKU


'''
创建索引
    如果你想针对某个app例如article做全文检索，则必须在article目录下面建立search_indexes.py文件，文件名不能修改。
    索引就像是一本书的目录，可以提供更快速的导航与查找。当数据量非常大的时候，若要从这些数据里查找所有满足搜索条件的几乎是不可能的，
    将会给服务器带来极大的负担。所以我们需要为指定的数据添加一个索引，索引的实现细节不需要关心，只需要关心为哪些字段创建索引，
    怎么指定

'''

class SKUIndex(indexes.SearchIndex, indexes.Indexable):
    """
    SKU索引数据模型
        1.类名必须为需要检索的Model_name+Index，这里需要检索SKU，所以创建SKUIndex
        2.每个索引里面必须有且只能有一个字段为 document=True，这代表haystack 和搜索引擎将使用此字段的内容作为索引进行检索(primary field)
        3.use_template =true 表示使用模板，这个模板的路径必须按照如下格式： templates/search/indexes/appname/model_text.txt ,
          如果不按照这个路径的话，就使用template_name 参数，指定模板文件,模板的内容就是我们索引所在的表字段，haystack 在这里面的字段上建立索引
    """

    # 在SKUIndex建立的字段, 都可以借助haystack由elasticsearch搜索引擎查询。
    # 其中text字段我们声明为document = True，表名该字段是主要进行关键字查询的字段，
    # 该字段的索引值可以由多个数据库模型类字段组成，具体由哪些模型类字段组成，我们用use_template = True表示后续通过模板来指明。

    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        """
        返回建立索引的模型类，返回建立索引的模型类，无需关注数据库读取、索引建立等细节。
        :return:
        """
        return SKU

    def index_queryset(self, using=None):
        """
        返回要建立索引的数据查询集
        :param using:
        :return:
        """
        return self.get_model().objects.filter(is_launched=True)