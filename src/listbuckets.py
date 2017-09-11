

from com.obs.client.obs_client import ObsClient


AK = 'SIQYC8WK9WFLUGFJUVI3'
SK = 'vneBIoLdfccFzq5FfYyOhC5LYjgRR8ChRPXqvtwO'
server = 'obs.myhwclouds.com'
region = 'china'
secure = False
signature = 'v4'
port = 80
path_style = True


'''
函数功能：初始化连接
函数原型： __init__(self, access_key_id, secret_access_key, is_secure=True, server=Utils.DEFAULT_HOST,
            signature='s3', region=None, path_style=True, ssl_verify=True): 
参数说明：access_key_id:AK值,secret_access_key：用于认证的SK的值,is_secure：是否使用SSl安全通道,取值（false,true）,
         server：obs服务器地址,signature:鉴权方式，取值为s3或v4,region:服务器所在区域，如果鉴权方式为v4,则必选，path_style：请求方式是否为绝对路径方式，
         取值True 或 False, ssl_verify:是否校验CA证书，取值True 或 False， port:HTTP/HTTPS请求的端口号
         max_retry_count:HTTP请求最大重试次数， timeout:单次http请求超时时间（单位：秒）
引入库: from com.obs.client.obs_client import ObsClient
返回值：对象实例句柄
'''
TestObs = ObsClient(access_key_id=AK, secret_access_key=SK, is_secure=secure, server=server, signature=signature, path_style=path_style, region=region,ssl_verify=False, port=port,
               max_retry_count=5, timeout=20, chuck_size=65536)

def initLog():
    '''
    函数功能：初始化日志
    函数原型：LogInit(logCog=LogConf())
    参数说明：logCog:日志配置文件信息,
    LogConf(confFile=None,sec=None),confFile:配置文件路径,sec：配置文件命名空间
    引入库: from com.obs.log.Log import *
    '''
    TestObs.initLog(LogConf('./log.conf'), 'test_client')  # 初始化obsclient日志
    LogInit(LogConf('./log.conf')) # 初始化global日志


def ListBuckets():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    函数原型： listBuckets(self)
    函数功能：查询桶列表
    参数说明:
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: ListBucketsResponse对象
    '''
    resp = TestObs.listBuckets()
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)

    listBcket = resp.body
    if listBcket:
        print('owner_id:', listBcket.owner.owner_id, ',owner_name:', listBcket.owner.owner_name)
        i = 0
        for item in listBcket.buckets:
            print('buckets[', i, ']:')
            print('backet_name:', item.name, ',create_date:', item.create_date)
            i += 1


if __name__ == '__main__':
    ListBuckets()