#coding=utf-8


from com.obs.client.obs_client import ObsClient

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

def DeleteObject(bucketname,fileName):
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    函数原型： deleteObject(self , bucketName, objectKey, versionId=None)
    函数功能：删除单个对象
    参数说明: bucketName：桶名 （必填）
    objectKey：对象名,
                如果是删除桶的一级目录的文件，直接指定如：1.txt
                如果是删除桶中的一个目录下的文件，指定对象为：test/1.txt
    versionId：对象版本号
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: None
    '''

    resp = TestObs.deleteObject(bucketName=bucketname, objectKey=fileName, versionId=None)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)


if __name__ == '__main__':
    DeleteObject('cxx','test1/1.txt')