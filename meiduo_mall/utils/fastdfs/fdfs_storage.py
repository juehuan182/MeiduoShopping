from fdfs_client.client import Fdfs_client
from django.conf import settings
from django.core.files.storage import Storage


class FastDFSStorage(Storage):
    """
    定义FastDFS客户端
    """
    def __init__(self, base_url=None, client_conf=None):
        """
        初始化对象
        :param base_url: 用于构造图片完整路径使用，图片服务器的域名
        :param client_conf: FastDFS客户端配置文件的路径
        """
        # if base_url is None:
        #     base_url = settings.FASTDFS_URL
        # self.base_url = base_url
        #
        # if client_conf is None:
        #     client_conf = settings.FASTDFS_CLIENT_CONF
        # self.client_conf = client_conf

        self.base_url = base_url or settings.FASTDFS_URL  # 技巧通过or来省去if的判断
        self.client_conf = client_conf or settings.FASTDFS_CLIENT_CONF

    def _open(self, name, mode='rb'):
        """
        存储系统打开文件存储的文件时调用此方法，因为我们自定义文件存储系统类，只是为了修改上传的目的，不需要打开，所以重写方法，什么也不做pass
        :param name: 打开文件的文件名
        :param mode: 打开文件的模式
        :return:
        """
        pass

    def _save(self, name, content):
        """
        上传文件时会调用此方法,重写此方法的目的,就是让文件上传到远程FastDFS服务器中
        :param name: 要上传的文件名
        :param content: 要上传的File对象 将来需要content.read() 文件二进制读取出并上传
        :return: 保存到数据库中的FastDFS的文件名
        """
        # 创建fastDFS客户端对象，指定fdfs客户端配置文件所在路径
        # client = Fdfs_client('/root/src/www/QmpythonBlog/util/fastdfs/client.conf')
        # client = Fdfs_client(settings.FASTDFS_CLIENT_CONF)
        client = Fdfs_client(self.client_conf)
        # 上传文件
        # client.upload_by_filename() # 如果有要上传文件的绝对路径才能使用此方法进行上传图片，并且用此方法上传的图片会有文件后缀
        # 如果要上传的是文件数据二进制数据流，可以用此方法上传文件，并且上传后没有后缀
        ret = client.upload_by_buffer(content.read())

        # 判断文件是否上传成功
        if ret.get('Status') != 'Upload successed.':
            # 返回失败
            raise Exception('Upload file failed')

        # 获取返回的文件ID
        file_id = ret.get('Remote file_id')  # 获取字典中的file_id

        return file_id

    def exists(self, name):
        """
        每次进行上传文件之前就会先调用此方法进行判断,当前要上传的文件是否已经在stroage服务器,如果在就不要上传了。
        FastDFS可以自行解决文件的重名问题，所以此处返回False，告诉Django上传的都是新文件
        :param name:   要进行判断是否上传的那个文件名
        :return: (文件已存在,不上传了) / False(文件不存在,可以上传)
        """
        return False


    def url(self, name):
        """
        当需要下载Storage服务器的文件时，就会调用此方法拼接出文件完整的下载路径
        :param name: 要下载的文件file_id
        :return: Storage服务器ip:端口 + file_id
        """
        return self.base_url + name

