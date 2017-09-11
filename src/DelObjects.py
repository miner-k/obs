#coding=utf-8

from com.obs.client.obs_client import ObsClient
from com.obs.models.delete_objects_request import Object,DeleteObjectsRequest

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


def DeleteObjects(bucketname):
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    from com.obs.models.delete_objects_request import Object,DeleteObjectsRequest
    函数原型： def deleteObjects(self, bucketName, deleteObjectsRequset)
    函数功能：批量删除对象
    参数说明: bucketName：桶名 （必填）
    deleteObjectsRequset：DeleteObjectsRequset 对象 批量删除对象列表请求
    Lobjects:是桶的对象的集合
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: DeleteObjectsResponse
    '''

    Lobject1 = Object(key='test1/1.png', versionId=None)
    # Lobject1.key:对象名
    # Lobject1.versionId:对象版本号
    #Lobject2 = Object(key='test.txt', versionId=None)
    #Lobject3 = Object(key='test', versionId=None)
    #Lobjects = [Lobject1, Lobject2, Lobject3]
    Lobjects = [Lobject1]

    Lreq = DeleteObjectsRequest(quiet=False, objects=Lobjects)
    # Lreq.quiet:用于指定使用quiet模式，只返回删除失败的对象结果；如果有此字段，则必被置为True，如果为False则被系统忽略掉。
    # Lreq.objects:待删除的对象列表

    resp = TestObs.deleteObjects(bucketName=bucketname, deleteObjectsRequest=Lreq)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body:
        if resp.body.deleted:
            i = 0
            for delete in resp.body.deleted:
                print('deleted[', i, ']:')
                i += 1
                print('key:', delete.key, ',deleteMarker:', delete.deleteMarker, ',deleteMarkerVersionId:', delete.deleteMarkerVersionId)
        if resp.body.error:
            i = 0
            for err in resp.body.error:
                print('error[', i, ']:')
                print('key:', err.key, ',code:', err.code, ',message:', err.message)



if __name__ == '__main__':
    DeleteObjects('cxx')