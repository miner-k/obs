#coding=utf-8

from com.obs.client.obs_client import ObsClient


AK = 'SIQYC8WK9WFLUGFJUVI3'
SK = 'vneBIoLdfccFzq5FfYyOhC5LYjgRR8ChRPXqvtwO'
server = 'obs.cn-east-2.myhwclouds.com'
region = 'china'
secure = False
signature = 'v4'
port = 80
path_style = True


TestObs = ObsClient(access_key_id=AK, secret_access_key=SK, is_secure=secure, server=server, signature=signature, path_style=path_style, region=region,ssl_verify=False, port=port,
               max_retry_count=5, timeout=20, chuck_size=65536)




def DeleteBucket(bucketname):
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    函数原型： deleteBucket(self,bucketName)
    函数功能：删除桶
   参数说明: bucketName：桶名 （必填）
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: None
    '''

    resp = TestObs.deleteBucket(bucketName=bucketname)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage, ',resHeader:', resp.header)


if __name__ == '__main__':
    DeleteBucket('cxxxx')