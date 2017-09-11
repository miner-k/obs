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




def PostObject(bucketname,dirName,filePath):
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    from com.obs.models.put_object_header import PutObjectHeader
    from com.obs.models.server_side_encryption import SseKmsHeader,SseCHeader
    函数原型：postObject(self, bucketName, objectKey, file_path, metadata=None, headers=None)
    函数功能：上传对象 （上传内容）
    参数说明: bucketName：桶名 （必填）
    objectKey:对象名
    dirName: 如果上传的是目录，该名称是保存到OBS桶中的名称
    
    file_path：上传文件路径,支持文件夹上传
    metadata：加入自定义的元数据，以便对对象进行自定义管理
    headers:附加消息头
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: None
   '''

    Lheaders = PutObjectHeader(md5=None, acl='private', location=None, contentType='text/plain')
    # Lheaders.md:对象的MD5值
    # Lheaders.acl:可以加上此消息头设置对象的权限控制策略，使用的策略为预定义的常用策略
    # Lheaders.location:当桶设置了Website配置，可以将获取这个对象的请求重定向到桶内另一个对象或一个外部的URL
    # Lheaders.contentType:对象的类型
    # Lheaders.sseHeader：服务端加密头信息

    # Lheaders.sseHeader = SseKmsHeader.getInstance()

    Lmetadata = {'key': 'value'}
    #file_path = r'C:\test.txt'

    resp = TestObs.postObject(bucketName=bucketname, objectKey=dirName, file_path=filePath,
                              metadata=Lmetadata, headers=Lheaders)
    if isinstance(resp, list):
        for k, v in resp:
            print('objectKey',k, 'common msg:status:', v.status, ',errorCode:', v.errorCode, ',errorMessage:', v.errorMessage)
    else:
        print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)


if __name__ == '__main__':
    PostObject('cxx','test1','C:\\abc')