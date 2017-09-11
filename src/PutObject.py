#coding=utf-8


from com.obs.client.obs_client import ObsClient
from com.obs.models.put_object_header import PutObjectHeader
from com.obs.models.server_side_encryption import SseKmsHeader,SseCHeader

AK = 'SIQYC8WK9WFLUGFJUVI3'
SK = 'vneBIoLdfccFzq5FfYyOhC5LYjgRR8ChRPXqvtwO'
server = 'obs.myhwclouds.com'
region = 'china'
secure = False
signature = 'v4'
port = 80
path_style = True


TestObs = ObsClient(access_key_id=AK, secret_access_key=SK, is_secure=secure, server=server, signature=signature, path_style=path_style, region=region,ssl_verify=False, port=port,
               max_retry_count=5, timeout=20, chuck_size=65536)


def PutObject(bucketname,fileName,fileContent):
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    from com.obs.models.put_object_header import PutObjectHeader
    from com.obs.models.server_side_encryption import SseKmsHeader,SseCHeader
    函数原型：putObject(self, bucketName, objectKey, content, metadata=None, headers=PutObjectHeader())
    函数功能：上传对象 （上传内容）
    参数说明: bucketName：桶名 （必填）
    objectKey:对象名
    content：对象内容
    metadata：加入自定义的元数据，以便对对象进行自定义管理
    headers:附加消息头
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: None
   '''
    sseHeader = SseKmsHeader.getInstance() #设置SSE-KMS加密
    #sseHeader = SseCHeader.getInstance(key='xxxxx') #设置SSE-C加密，传入密钥
    #Lheaders = PutObjectHeader(md5=None, acl='private', location=None, contentType='text/plain', sseHeader=sseHeader)
    Lheaders = PutObjectHeader(md5=None, acl='private', location=None, contentType='image/png')

    # contentType :'text/plain' 文本 image/png png格式的图片 image/jpeg jpeg格式的图片
    # Lheaders.md:对象的MD5值
    # Lheaders.acl:可以加上此消息头设置对象的权限控制策略，使用的策略为预定义的常用策略
    # Lheaders.location:当桶设置了Website配置，可以将获取这个对象的请求重定向到桶内另一个对象或一个外部的URL

    Lmetadata = {'key': 'value'}

    resp = TestObs.putObject(bucketname, objectKey=fileName, content=fileContent,
                             metadata=Lmetadata, headers=Lheaders)

    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    print(resp.header)


if __name__ == '__main__':
    # PutObject('cxx')


    with open('1.png','rb') as f1:
        PutObject('cxx','2.png',f1.read())