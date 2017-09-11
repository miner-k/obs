#coding=utf-8

from com.obs.client.obs_client import ObsClient
from com.obs.models.create_bucket_header import CreateBucketHeader
from com.obs.models.head_permission import HeadPermission


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



def CreateBucket(bucketName,region='cn-north-1',bucketClass='STANDARD_IA'):
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    from com.obs.models.creat_bucket_header import CreateBucketHeader
    from com.obs.models.head_permission import HeadPermission
    函数原型： createBucket(self, bucketName, header=CreateBucketHeader(), location=None)
    函数功能：创建桶
    参数说明: bucketName：桶名 （必填）
    header:CreateBucketHeader对象（选填）,
    region：设置桶所在数据中心（选填）cn-north-1/cn-south-1/cn-south-1
    bucketClass:桶的存储类别，STANDARD（标准存储）、STANDARD_IA（低频访问存储）、GLACIER（归档存储）
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: None
    '''

    headers = CreateBucketHeader(aclControl=HeadPermission.PUBLIC_READ, storageClass=bucketClass)
    # headers.aclControl :x-amz-acl 对应值 （HeadPermission对象的枚举）
    # headers.storageClass :x-default-storage-class 对应值，当OBS服务开启了storage_class_enable开关后，该参数用来创建不同默认存储类型的桶，
    # 桶内对象的存储类型与桶默认存储类型保持一致。存储类型有3种：STANDARD（标准存储）、STANDARD_IA（近线存储）、GLACIER（归档存储），默认值为STANDARD（标准存储）

    resp = TestObs.createBucket(bucketName, header=headers, location=region)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage, ',resHeader:', resp.header)


if __name__ == "__main__":
    CreateBucket('cxxxx','cn-east-2')