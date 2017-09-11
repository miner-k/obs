#!/usr/bin/python
# -*- coding:utf-8 -*-

from com.obs.client.obs_client import ObsClient
from com.obs.models.create_bucket_header import CreateBucketHeader
from com.obs.models.head_permission import HeadPermission
from com.obs.models.grant import Grant,Permission
from com.obs.models.grantee import Grantee,Group
from com.obs.models.owner import Owner
from com.obs.models.acl import ACL
from com.obs.models.versions import Versions
from com.obs.models.rule import Rule
from com.obs.models.lifecycle import Lifecycle
from com.obs.models.expiration import Expiration,NoncurrentVersionExpiration
from com.obs.models.date_time import DateTime
from com.obs.models.condition import Condition
from com.obs.models.redirect import Redirect
from com.obs.models.routing_rule import RoutingRule
from com.obs.models.error_document import ErrorDocument
from com.obs.models.index_document import IndexDocument
from com.obs.models.redirect_all_request_to import RedirectAllRequestTo
from com.obs.models.website_configuration import WebsiteConfiguration
from com.obs.models.tag import TagInfo
from com.obs.models.logging import Logging
from com.obs.models.cors_rule import CorsRule
from com.obs.models.options import Options
from com.obs.models.notification import Notification, FilterRule
from com.obs.models.delete_objects_request import DeleteObjectsRequest,Object
from com.obs.models.restore import TierType
from com.obs.models.complete_multipart_upload_request import CompleteMultipartUploadRequest, CompletePart
from com.obs.models.list_multipart_uploads_request import ListMultipartUploadsRequest
from com.obs.models.put_object_header import PutObjectHeader
from com.obs.models.copy_object_header import CopyObjectHeader
from com.obs.models.get_object_header import GetObjectHeader
from com.obs.models.get_object_request import GetObjectRequest
from com.obs.response.get_result import ObjectStream
from com.obs.models.server_side_encryption import SseKmsHeader,SseCHeader
from com.obs.log.Log import *


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


def CreateBucket():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    from com.obs.models.creat_bucket_header import CreateBucketHeader
    from com.obs.models.head_permission import HeadPermission
    函数原型： createBucket(self, bucketName, header=CreateBucketHeader(), location=None)
    函数功能：创建桶
    参数说明: bucketName：桶名 （必填）
    header:CreateBucketHeader对象（选填）,
    location：设置桶所在数据中心（选填）
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: None
    '''

    headers = CreateBucketHeader(aclControl=HeadPermission.PUBLIC_READ, storageClass='STANDARD_IA')
    # headers.aclControl :x-amz-acl 对应值 （HeadPermission对象的枚举）
    # headers.storageClass :x-default-storage-class 对应值，当OBS服务开启了storage_class_enable开关后，该参数用来创建不同默认存储类型的桶，
    # 桶内对象的存储类型与桶默认存储类型保持一致。存储类型有3种：STANDARD（标准存储）、STANDARD_IA（近线存储）、GLACIER（归档存储），默认值为STANDARD（标准存储）

    resp = TestObs.createBucket(bucketName='bucket001', header=headers, location=None)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage, ',resHeader:', resp.header)


def DeleteBucket():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    函数原型： deleteBucket(self,bucketName)
    函数功能：删除桶
   参数说明: bucketName：桶名 （必填）
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: None
    '''

    resp = TestObs.deleteBucket(bucketName='bucket001')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage, ',resHeader:', resp.header)


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

def HeadBucket():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    函数原型： headBucket(self,bucketName)
    函数功能：head 桶
    参数说明: bucketName：桶名 （必填）
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: None
    '''

    resp = TestObs.headBucket(bucketName='bucket001')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage, ',resHeader:', resp.header)

def GetBucketMetadata():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    函数原型： getBucketMetadata(self, bucketName, origin=None, requestHeaders=None)
    函数功能：获取桶元数据信息
    参数说明: bucketName：桶名 （必填）
    origin：预请求指定的跨域请求 (选填)
    requestHeaders: 实际请求可以带的HTTP头域（选填）
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: None
    '''
    resp = TestObs.getBucketMetadata(bucketName='bucket001',origin='www.example.com', requestHeaders='header1')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    header = dict(resp.header)
    print(header.get('x-default-storage-class'))
    print(header.get('access-control-allow-origin'))
    print(header.get('access-control-allow-headers'))
    print(header.get('access-control-max-age'))
    print(header.get('access-control-allow-methods'))
    print(header.get('access-control-expose-headers'))


def SetBucketQuota():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    函数原型：setBucketQuota(self , bucketName, quota)
    函数功能：更新桶配额
    参数说明: bucketName：桶名 （必填）
    quota:指定桶空间配额值
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: None
    '''

    resp = TestObs.setBucketQuota(bucketName='bucket001', quota=1048576 * 600)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)


def GetBucketQuota():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    函数原型：getBucketQuota(self , bucketName)
    函数功能：获取桶配额信息
    参数说明: bucketName：桶名 （必填）
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: GetBucketQuotaResponse
    '''

    resp = TestObs.getBucketQuota(bucketName='bucket001')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body:
        print('quota:', resp.body.quota)


def GetBucketStorageInfo():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    函数原型：getBucketStorageInfo(self , bucketName)
    函数功能：获取桶存量
    参数说明: bucketName：桶名 （必填）
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: GetBucketStorageInfoResponse
    '''

    resp = TestObs.getBucketStorageInfo(bucketName='bucket001')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body:
        print('size:', resp.body.size, ',objectNumber:', resp.body.objectNumber)


def SetBucketAcl():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    from com.obs.models.acl import ACL
    from com.obs.models.grant import Grant,Permission
    from com.obs.models.grantee import Grantee,Group
    from com.obs.models.head_permission import HeadPermission
    from com.obs.models.owner import Owner
    函数原型： setBukcetAcl(self,bucketName,acl=ACL(),x_amz_acl=None)
    函数功能：设置桶ACL
    参数说明: bucketName：桶名 （必填）
    acl：ACL对象（ACL策略）
    x_amz_acl：x-amz-acl 对象值（HeadPermission对象的枚举,和acl不能同时存在）
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: None
    '''

    Lowner = Owner(owner_id='806BxxxxADB', owner_name='user')
    # Lowner.owner_id: 桶拥有者的用户ID
    # Lowner.owner_name: 桶拥有者的用户名

    Lgrantee1 = Grantee(grantee_id='806BxxxxAADB', grantee_name='user', group=None)
    # Lgrantee1.grantee_id:被授权用户ID
    # Lgrantee1.grantee_name:被授权用户名
    # Lgrantee1.group:被授权用户组
    Lgrantee2 = Grantee(group=Group.LOG_DELIVERY)

    Lgrant1 = Grant(grantee=Lgrantee1, permission=Permission.READ)
    # Lgrant1.grantee:Grantee对象值
    # Lgrant1.permission:权限值 (Permission对象枚举值)
    Lgrant2 = Grant(grantee=Lgrantee2, permission=Permission.READ_ACP)
    Lgrant3 = Grant(grantee=Lgrantee2, permission=Permission.WRITE)
    Lgrants = [Lgrant1, Lgrant2, Lgrant3]

    Lacl = ACL(owner=Lowner, grants=Lgrants)
    # Lacl.owner  资源拥有者 (Owner对象）
    # Lacl.grants 访问控制列表（Grant列表）

    resp = TestObs.setBucketAcl(bucketName='bucket001', acl=Lacl, x_amz_acl=None)
    # resp = TestObs.setBucketAcl(bucketName='bucket001', acl=None, x_amz_acl=HeadPermission.PUBLIC_READ_WRITE)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)


def GetBucketAcl():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    函数原型： getBucketAcl(self,bucketName)
    函数功能：设置桶ACL
    参数说明: bucketName：桶名 （必填）
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: ACL对象
    '''

    resp = TestObs.getBucketAcl(bucketName='bucket001')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body:
        print('owner_id:', resp.body.owner.owner_id, ',owner_name:', resp.body.owner.owner_name)
        i = 0
        for grant in resp.body.grants:
            print('grants[', i, ']:')
            print('permission:', grant.permission)
            print('grantee_name:', grant.grantee.grantee_name, ',grantee_id:', grant.grantee.grantee_id, ',group:', grant.grantee.group)
            i += 1


def SetBucketPolicy():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    函数原型： setBucketPolicy(self,bucketName,policyJSON)
    函数功能：设置桶的策略
    参数说明: bucketName：桶名 （必填）
    policyJSON：桶的策略 ,只支持'Version':'2008-10-17',格式参照http://docs.aws.amazon.com/AmazonS3/latest/dev/AccessPolicyLanguage_HowToWritePolicies.html
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: None
    '''

    LpolicyJSON = '''{'Version':'2008-10-17','Id': 'Policy1375342051334','Statement': [{'Sid': 'Stmt1375240018061','Action': ['s3:GetBucketPolicy'],'Effect': 'Allow','Resource': 'arn:aws:s3:::bucket','Principal': { 'AWS': ['*'] } }]}'''
    resp = TestObs.setBucketPolicy(bucketName='bucket001', policyJSON=LpolicyJSON)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)


def GetBucketPolicy():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    函数原型： getBucketPolicy(self,bucketName)
    函数功能：获取桶的策略
    参数说明: bucketName：桶名 （必填）
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body:Policy 对象（桶的策略）
    '''

    resp = TestObs.getBucketPolicy(bucketName='bucket001')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body:
        print('policyJSON:', resp.body)

def DeleteBucketPolicy():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    函数原型： getBucketPolicy(self,bucketName)
    函数功能：删除桶的策略
    参数说明: bucketName：桶名 （必填）
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: None
    '''

    resp = TestObs.deleteBucketPolicy(bucketName='bucket001')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)

def SetBucketVersioningConfiguration():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    函数原型： setBucketVersioningConfiguration(self,bucketName,status=None)
    函数功能：设置桶的多版本状态
    参数说明: bucketName：桶名 （必填）
    status:桶的状态 (取值为：Enabled或Suspended)
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: None
    '''

    resp = TestObs.setBucketVersioningConfiguration(bucketName='bucket001', status='Enabled')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)

def  GetBucketVersioningConfiguration():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    函数原型： getBucketVersioningConfiguration(self,bucketName)
    函数功能：获取桶的多版本状态
    参数说明: bucketName：桶名 （必填）
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: 字符串(桶的 多版本状态)
    '''

    resp = TestObs.getBucketVersioningConfiguration(bucketName='bucket001')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    print('status:', resp.body)


def ListVersions():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    from com.obs.models.versions import Versions
    函数原型：listVersions(self,bucketName,version=None)
    函数功能：获取桶内对象多版本信息
    参数说明: bucketName：桶名 （必填）
    version:Versions对象,查新条件
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: ObjectVersions 对象
    '''

    Lversion = Versions(prefix=None, key_marker=None, max_keys=2, delimiter=None, version_id_marker=None)
    # version.prefix:列举以指定的字符串prefix开头的对象
    # version.key_marker:返回的对象列表将是按照字典顺序排序后在这个标识符以后的所有对象
    # version.max_keys:返回的最大对象数
    # version.delimiter:字符串delimiter的第一个字符和字符串prefix之间的字符序列如果相同,则这部分字符序列合并在一起,在返回信息的CommonPrefixes节点显示
    # version.version_id_marker:与key-marker配合使用,返回的对象列表将是按照字典顺序排序后在该标识符以后的所有对象

    resp = TestObs.listVersions(bucketName='bucket001', version=Lversion)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body:
        print('name:', resp.body.head.name, ',prefix:', resp.body.head.prefix, ',keyMarker:', resp.body.head.keyMarker, ',maxKeys:', resp.body.head.maxKeys)
        print('nextKeyMarker:', resp.body.head.nextKeyMarker, ',nextVersionIdMarker:', resp.body.head.nextVersionIdMarker, ',versionIdMarker:', resp.body.head.versionIdMarker, ',isTruncated:', resp.body.head.isTruncated)
        i = 0
        for version in resp.body.versions:
            print('versions[', i, ']:')
            print('owner_id:', version.owner.owner_id, ',owner_name:', version.owner.owner_name)
            print('key:', version.key)
            print('lastModified:', version.lastModified, ',versionId:', version.versionId, ',eTag:', version.eTag, ',storageClass:', version.storageClass, ',isLatest:', version.isLatest, ',size:', version.size)
            i += 1
            pass
        i = 0
        for marker in resp.body.markers:
            print('markers[', i, ']:')
            print('owner_id:', marker.owner.owner_id, ',owner_name:', marker.owner.owner_name)
            print('key:', marker.key)
            print('key:', marker.key, ',versionId:', marker.versionId, ',isLatest:', marker.isLatest, ',lastModified:', marker.lastModified)
            i += 1
        i = 0
        for Prefix in resp.body.commonPrefixs:
            print('commonPrefixs[', i, ']')
            print('prefix:', Prefix.prefix)
            i += 1

def ListObjects():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    函数原型：listObjects(self,bucketName,prefix=None,marker=None,max_keys=None,delimiter=None)
    函数功能：获取桶内对象
    参数说明: bucketName：桶名 （必填）
    prefix:列举以指定的字符串prefix开头的对象
    marker:返回的对象列表将是按照字典顺序排序后这个标识符以后的所有对象
    max_keys:指定返回的最大对象数
    delimiter:用来分组桶内对象的字符串
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: ObjectVersions 对象
    '''
    resp = TestObs.listObjects(bucketName='bucket001', prefix=None, marker=None, max_keys=2, delimiter=None)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body:
        print('name:', resp.body.name, ',prefix:', resp.body.prefix, ',marker:', resp.body.marker, ',max_keys:', resp.body.max_keys)
        print('delimiter:', resp.body.delimiter, ',is_truncated:', resp.body.is_truncated, ',next_marker:', resp.body.next_marker)
        i = 0
        for content in resp.body.contents:
            print('contents[', i, ']:')
            print('owner_id:', content.owner.owner_id, ',owner_name:', content.owner.owner_name)
            print('key:', content.key, ',lastmodified:', content.lastmodified, ',etag:', content.etag, ',size:', content.size, ',storageClass:', content.storageClass)
            i += 1
        i = 0
        for prefix in resp.body.commonprefixs:
            print('commonprefixs[', i, ']:')
            print('prefix:', prefix.prefix)
            i += 1


def SetBucketLifecycleConfiguration():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    from com.obs.models.date_time import DateTime
    from com.obs.models.expiration import Expiration
    from com.obs.models.rule import Rule
    from com.obs.models.lifecycle import Lifecycle
    函数原型：setBucketLifecycleConfiguration(self,bucketName,lifecycle)
    函数功能：设置桶的生命周期
    参数说明: bucketName：桶名 （必填）
    lifcycle:Lifecycle对象,生命周期配置
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: None
    '''

    Lexpiration = Expiration(date=DateTime(2030, 6, 10), days=None)
    # Lexpiration.date:过期时间,可以为UTC时间格式的字符串（如：date='2015-04-30T00:00:00.000Z'）,也可以是DateTime对象,和days不能同时设置
    # Lexpiration.days：多少天后过期,和date不能同时设置

    noncurrentVersionExpiration = NoncurrentVersionExpiration(noncurrentDays=10)

    Lrule = Rule(id='101', prefix='test', status='Enabled', expiration=Lexpiration, noncurrentVersionExpiration=noncurrentVersionExpiration)
    # Lrule.id:一条Rule的标识,由不超过255个字符的字符串组成
    # Lrule.prefix:对象名前缀,用以标识哪些对象可以匹配到当前这条Rule
    # Lrule.status:标识当前这条Rule是否启用,有效值：Enabled,Disabled
    # Lrule.expiration:Expiration对象

    Lrules = [Lrule]
    Llifecycle = Lifecycle(rule=Lrules)
    # Llifecycle.rule:Rule对象的数组

    resp = TestObs.setBucketLifecycleConfiguration(bucketName='bucket001', lifecycle=Llifecycle)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)


def GetBucketLifecycleConfiguration():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    函数原型：getBucketLifecycleConfiguration(self, bucketName):
    函数功能：设置桶的生命周期
    参数说明: bucketName：桶名 （必填）
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: LifecycleResponse 对象
    '''

    resp = TestObs.getBucketLifecycleConfiguration(bucketName='bucket001')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body:
        i = 0
        for rule in resp.body.lifecycleConfig.rule:
            print('rule[', i, ']:')
            print('id:', rule.id, ',prefix:', rule.prefix, ',status:', rule.status, ',date:', rule.expiration.date, ',days:', rule.expiration.days)
            print('nocurrentDays:', rule.noncurrentVersionExpiration)
            i += 1

def DeleteBucketLifecycleConfiguration():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    函数原型：deleteBucketLifecycleConfiguration(self, bucketName)
    函数功能：删除桶的生命周期
    参数说明: bucketName：桶名 （必填）
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: None
   '''

    resp = TestObs.deleteBucketLifecycleConfiguration(bucketName='bucket001')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)


def SetBucketWebsiteConfiguration():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    from com.obs.models.redirect_all_request_to import RedirectAllRequestTo
    from com.obs.models.index_document import IndexDocument
    from com.obs.models.condition import Condition
    from com.obs.models.redirect import Redirect
    from com.obs.models.website_configuration import WebsiteConfiguration
    from com.obs.models.error_document import ErrorDocument
    from com.obs.models.routing_rule import RoutingRule
    函数原型：setBucketWebsiteConfiguration(self,bucketName,website)
    函数功能：设置桶的网络配置
    参数说明: bucketName：桶名 （必填）
    website:WebsiteConfiguration对象,桶的网络配置信息
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: None
    '''

    Lweb = RedirectAllRequestTo(hostName='www.xxx.com', protocol='http')
    # Lweb.hostName:描述重定向的站点名
    # Lweb.Protocol:描述重定向请求时使用的协议（http,https）,默认使用http协议

    Lindex = IndexDocument(suffix='index.html')
    # Lindex.suffix:Suffix 元素被追加在对文件夹的请求的末尾（例如：Suffix 配置的是“index.html”,请求的是“samplebucket/images/”,返回的数据将是“samplebucket”桶内名为“images/index.html”的对象的内容）

    Lerr = ErrorDocument(key='error.html')
    # Lerr.key:当4XX错误出现时使用的对象的名称。这个元素指定了当错误出现时返回的页面

    Lcondition = Condition(keyPrefixEquals=None, httpErrorCodeReturnedEquals=404)
    # Lcondition.keyPrefixEquals:描述当重定向生效时对象名的前缀
    # Lcondition.httpErrorCodeReturnedEquals:描述Redirect生效时的HTTP错误码。当发生错误时,如果错误码等于这个值,那么Redirect生效,和KeyPrefixEquals不同时存在

    Lredirect = Redirect(protocol='http', hostName=None, replaceKeyPrefixWith=None, replaceKeyWith='NotFound.html',
                         httpRedirectCode=None)
    # Lredirect.protocol:描述重定向请求时使用的协议
    # Lredirect.hostName:描述重定向请求时使用的站点名
    # Lredirect.replaceKeyPrefixWith:描述重定向请求时使用的对象名前缀
    # Lredirect.replaceKeyWith:描述重定向请求时使用的对象名
    # Lredirect.httpRedirectCode:描述响应中的HTTP状态码

    Lrout = RoutingRule(condition=Lcondition, redirect=Lredirect)
    # Lrout.condition:Condition对象
    # Lrout.redirect:Redirect对象

    Lrouts = [Lrout, Lrout]
    Lwebsite = WebsiteConfiguration(redirectAllRequestTo=None, indexDocument=Lindex, errorDocument=Lerr,
                                    routingRules=Lrouts)
    # Lwebsite.redirectAllRequestTo:RedirectAllRequestTo对象,和另外3个参数不能共存
    # Lwebsite.indexDocument:IndexDocument对象
    # Lwebsite.errorDocument:ErrorDocument对象
    # Lwebsite.routingRules:RoutingRule对象的链表

    resp = TestObs.setBucketWebsiteConfiguration(bucketName='bucket001', website=Lwebsite)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)


def GetBucketWebsiteConfiguration():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    函数原型：getBucketWebsiteConfiguration(self,bucketName)
    函数功能：获取桶的网络配置
    参数说明: bucketName：桶名 （必填）
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: BucketWebsite 对象
    '''

    resp = TestObs.getBucketWebsiteConfiguration(bucketName='bucket001')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body:
        if resp.body.redirectAllRequestTo:
            print('redirectAllRequestTo.hostName:', resp.body.redirectAllRequestTo.hostName, ',redirectAllRequestTo.Protocol:', resp.body.redirectAllRequestTo.Protocol)
        if resp.body.indexDocument:
            print('indexDocument.suffix:', resp.body.indexDocument.suffix)
        if resp.body.errorDocument:
            print('errorDocument.key:', resp.body.errorDocument.key)
        if resp.body.routingRules:
            i = 0
            for rout in resp.body.routingRules:
                print('routingRule[', i, ']:')
                i += 1
                print('condition.keyPrefixEquals:', rout.condition.keyPrefixEquals, ',condition.httpErrorCodeReturnedEquals:', rout.condition.httpErrorCodeReturnedEquals)
                print('redirect.protocol:', rout.redirect.protocol, ',redirect.hostName:', rout.redirect.hostName, ',redirect.replaceKeyPrefixWith:', rout.redirect.replaceKeyPrefixWith, ',redirect.replaceKeyWith:', rout.redirect.replaceKeyWith, ',redirect.httpRedirectCode:', rout.redirect.httpRedirectCode)

def DeleteBucketWebsiteConfiguration():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    函数原型：deleteBucketWebsiteConfiguration(self, bucketName)
    函数功能：删除桶的网络配置
    参数说明: bucketName：桶名 （必填）
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: None
    '''

    resp = TestObs.deleteBucketWebsiteConfiguration(bucketName='bucket001')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)


def SetBucketLoggingConfiguration():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    from com.obs.models.logging import Logging
    from com.obs.models.grant import Grant,Permission
    from com.obs.models.grantee import Grantee,Group
    函数原型：setBucketLoggingConfiguration(self, bucketName, logstatus)
    函数功能：设置桶的日志管理
    参数说明: bucketName：桶名 （必填）
    logstatus：桶的日志管理信息
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: None
    '''

    Lgrantee = Grantee(grantee_id='806xxxxAADB', grantee_name='user', group=None)
    # Lgrantee.grantee_id:被授权者的CanonicalUserId，全局唯一标识
    # Lgrantee.grantee_name:被授权用户的名称
    # Lgrantee.group:被授权的用户组，不能和另两个参数并存，取值为Group对象的枚举
    Lgrantee1 = Grantee(grantee_id=None, grantee_name=None, group=Group.ALL_USERE)

    Lgrant1 = Grant(grantee=Lgrantee, permission=Permission.WRITE)
    # Lgrant.grantee:Grantee对象
    # Lgrant.permission:授予的权限，Permission对象的枚举
    Lgrant2 = Grant(grantee=Lgrantee1, permission=Permission.READ)

    LgrantList = [Lgrant1, Lgrant2]
    Llog = Logging(targetBucket='bucket002', targetPrefix='log_1', targetGrants=LgrantList)
    # Llog.targetBucket:日志生产的目标桶，该桶必须要有日志投递用户组对该桶的WRITE和READ_ACP权限
    # Llog.targetPrefix:通过该元素指定一个前缀，生成的日志对象的对象名都以此元素的内容为前缀
    # Llog.targetGrants:Grant对象链表

    resp = TestObs.setBucketLoggingConfiguration(bucketName='bucket001', logstatus=Llog)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)


def GetBucketLoggingConfiguration():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    函数原型：getBucketLoggingConfiguration(self, bucketName)
    函数功能：获取桶的日志配置信息
    参数说明: bucketName：桶名 （必填）
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: Logging 对象
    '''

    resp = TestObs.getBucketLoggingConfiguration(bucketName='bucket001')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body:
        print('targetBucket:', resp.body.targetBucket, 'targetPrefix:', resp.body.targetPrefix)
        i = 0
        for grant in resp.body.targetGrants:
            print('targetGrant[', i, ']:')
            i += 1
            print('permission:', grant.permission, ',grantee.grantee_id:', grant.grantee.grantee_id, ',grantee.grantee_name:', grant.grantee.grantee_name, ',grantee.group:', grant.grantee.group)


def GetBucketLocation():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    函数原型：getBucketLocation(self, bucketName)
    函数功能：获取桶的数据中心
    参数说明: bucketName：桶名 （必填）
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: LocationResponce 对象
    '''

    resp = TestObs.getBucketLocation(bucketName='bucket001')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body:
        print('location:', resp.body.location)

def SetBucketTagging():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    from com.obs.models.tag import TagInfo
    函数原型： setBucketTagging(self,bucketName,tagInfo):
    函数功能：设置桶标签
    参数说明: bucketName：桶名 （必填）
            tagInfo：桶标签信息（必填）
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: None
    '''
    tagInfo = TagInfo()
    tagInfo.addTag('testKey1','testValue1').addTag('testKey2','testValue2')
    resp = TestObs.setBucketTagging(bucketName='bucket001',tagInfo=tagInfo)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)

def DeleteBucketTagging():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    函数原型： deleteBucketTagging(self,bucketName):
    函数功能：设置桶标签
    参数说明: bucketName：桶名 （必填）
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: None
    '''
    resp = TestObs.deleteBucketTagging('bucket001')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)

def GetBucketTagging():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    from com.obs.models.tag import TagInfo
    函数原型： getBucketTagging(self,bucketName):
    函数功能：设置桶标签
    参数说明: bucketName：桶名 （必填）
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: TagInfo对象
    '''
    resp = TestObs.getBucketTagging('bucket001')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    for tag in resp.body.tagSet:
        print('{0}:{1}'.format(tag.key,tag.value))


def SetBucketCors():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    from com.obs.models.cors_rule import CorsRule
    函数原型： setBucketCors(self, bucketName, corsRule)
    函数功能：设置桶的CORS
    参数说明: bucketName：桶名 （必填）
    corsRule：CorsRule对象
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: None
    '''
    cors1 = CorsRule(id='101', allowedMethod=['PUT', 'POST', 'GET', 'DELETE'],
                     allowedOrigin=['www.xxx.com', 'www.x.com'], allowedHeader=['header-1', 'header-2'],
                     maxAgeSecond=100, exposeHeader=['head1'])
    cors2 = CorsRule(id='102', allowedMethod=['PUT', 'POST', 'GET', 'DELETE'],
                     allowedOrigin=['www.xxx.com', 'www.x.com'], allowedHeader=['header-1', 'header-2'],
                     maxAgeSecond=100, exposeHeader=['head1'])

    corsList = [cors1, cors2]

    resp = TestObs.setBucketCors('bucket001', corsList)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)

def GetBucketCors():
    '''
    引入库:from com.obs.client.obs_client import ObsClient
    from com.obs.models.cors_rule import CorsRule
    函数原型： getBucketCors(self, bucketName)
    函数功能：获取桶的CORS
    参数说明: bucketName：桶名 （必填）
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: CorsRule
    '''

    resp = TestObs.getBucketCors('bucket001')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body is not None:
        for v in resp.body:
            print(v)


def DeleteBucketCors():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    函数原型： deleteBucketCors(self, bucketName)
    函数功能：删除桶的CORS
    参数说明: bucketName：桶名 （必填）
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: None
    '''

    resp = TestObs.deleteBucketCors('bucket001')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)


def OptionsBucket():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    from com.obs.models.options import Options
    函数原型： optionBucket(self,bucketName,option=Options())
    函数功能：OPTIONS桶
    参数说明: bucketName：桶名 （必填）
    option：Options对象
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: OptionsResp
    '''
    option = Options(origin='www.example.com', accessControlRequestMethods=['GET', 'POST'],
                     accessControlRequestHeaders=['header1', 'header2'])
    resp = TestObs.optionsBucket('bucket001', option)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body is not None:
        print(resp.body)

def OptionsObject():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    from com.obs.models.options import Options
    函数原型： optionObject(self,bucketName,objectKey,option=None)
    函数功能：OPTIONS桶
    参数说明: bucketName：桶名 （必填）
    objectKey:对象名(必填)
    option：Options对象
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: OptionsResp
    '''
    option = Options(origin='www.example.com', accessControlRequestMethods=['PUT'])
    resp = TestObs.optionsObject('bucket001', 'test.txt', option)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body is not None:
        print(resp.body)

def SetBucketNotification():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    from com.obs.models.notification import Notification, FilterRule
    函数原型： setBucketNotification(self, bucketName, notification)
    函数功能：设置桶的通知配置
    参数说明: bucketName：桶名 （必填）
    notification：Notification
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: None
    '''
    fr1 = FilterRule(name='prefix', value='smn')
    fr2 = FilterRule(name='suffix', value='.jpg')
    notification = Notification(id='001',topic='urn:smn:region3:35667523534:topic1',events=['s3:ObjectCreated:*'], filterRules=[fr1,fr2])
    resp = TestObs.setBucketNotification('bucket001', notification)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)

def GetBucketNotification():
    '''
    引入库:from com.obs.client.obs_client import ObsClient
    from com.obs.models.notification import Notification, FilterRule
    函数原型： getBucketNotification(self, bucketName)
    函数功能：获取桶的通知配置
    参数说明: bucketName：桶名 （必填）
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: Notification
    '''

    resp = TestObs.getBucketNotification('bucket001')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body is not None:
        print(resp.body)


def ListMultipartUploads():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    from com.obs.models.list_multipart_uploads_request import ListMultipartUploadsRequest
    函数原型：listMultipartUploads(self, bucketName, multipart=ListMultipartUploadsRequest())
    函数功能：列出多段上传任务
    参数说明: bucketName：桶名 （必填）
    multipart:ListMultipartUploadsRequest对象
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: ListMultipartUploadsResponse 对象
    '''

    Lmultipart = ListMultipartUploadsRequest(delimiter=None, prefix=None, max_uploads=10, key_marker=None,
                                             upload_id_marker=None)
    # Lmultipart.delimiter:对于名字中包含delimiter的对象的任务，其对象名（如果请求中指定了prefix，则此处的对象名需要去掉prefix）中从首字符至第一个delimiter之间的字符串将作为CommonPrefix在响应中返回
    # Lmultipart.prefix:如果请求中指定了prefix，则响应中仅包含对象名以prefix开始的任务信息
    # Lmultipart.max_uploads:列举的多段任务的最大条目，取值范围为[1,1000]
    # Lmultipart.key_marker:列举时返回指定的key-marker之后的多段任务
    # Lmultipart.upload_id_marker:只有和key-marker一起使用才有意义， 列举时返回指定的key-marker的upload-id-marker之后的多段任务

    resp = TestObs.listMultipartUploads(bucketName='bucket001', multipart=Lmultipart)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body:
        print('bucket:', resp.body.bucket, ',keyMarker：', resp.body.keyMarker, 'uploadIdMarker:', resp.body.uploadIdMarker, ',nextKeyMarker：', resp.body.nextKeyMarker, 'delimiter:', resp.body.delimiter)
        print('nextUploadIdMarker:', resp.body.nextUploadIdMarker, ',maxUploads：', resp.body.maxUploads, 'isTruncated:', resp.body.isTruncated, ',prefix：', resp.body.prefix)
        if resp.body.upload:
            i = 0
            for upload in resp.body.upload:
                print('upload[', i, ']:')
                i += 1
                print('key:', upload.key, ',uploadID:', upload.uploadID, ',storageClass:', upload.storageClass, ',initiated:', upload.initiated)
                if upload.owner:
                    print('owner.owner_id:', upload.owner.owner_id, ',owner.owner_name:', upload.owner.owner_name)
                if upload.initiator:
                    print('initiator.id:', upload.initiator.id, 'initiator.name:', upload.initiator.name)
        if resp.body.commonPrefixs:
            i = 0
            for commonPrefix in resp.body.commonPrefixs:
                print('commonPrefix[', i, ']:')
                i += 1
                print('prefix:', commonPrefix.prefix)


def SetObjectAcl():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    from com.obs.models.acl import ACL
    from com.obs.models.head_permission import HeadPermission
    from com.obs.models.grant import Grant,Permission
    from com.obs.models.grantee import Grantee,Group
    from com.obs.models.owner import Owner
    函数原型：setObjectAcl(self , bucketName, objectKey, acl=ACL(), versionId=None, aclControl=None)
    函数功能:设置对象的ACL
    参数说明: bucketName：桶名 （必填）
    objectKey:对象名
    acl：ACL对象名
    versionId: 对象的版本号
    aclControl:附加头域x-amz-acl值
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: None
   '''

    Lowner = Owner(owner_id='B67ExxxxDE62C', owner_name='usr')
    # Lowner.owner_id：桶拥有者的ID
    # Lowner.owner_name:桶拥有者名

    Lgrantee = Grantee(grantee_id='729AxxxxFBBDF', grantee_name='usr', group=None)

    # Lgrantee.grantee_id: 被授权用户ID
    # Lgrantee.grantee_name:被授权用户名
    # Lgrantee.group:被授权用户组

    Lgrant = Grant(grantee=Lgrantee, permission=Permission.READ)
    # Lgrant.grantee:Grantee对象
    # Lgrant.permission:被授予的权限，Permission对象的枚举

    Lgrants = [Lgrant]

    Lacl = ACL(owner=Lowner, grants=Lgrants)
    # Lacl.owner:Owner对象
    # Lacl.grants:Grant对象链表

    resp = TestObs.setObjectAcl(bucketName='bucket001', objectKey='test.txt', acl=None, versionId=None,
                                aclControl=HeadPermission.PUBLIC_READ_WRITE)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)

def GetObjectAcl():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    函数原型： getObjectAcl(self, bucketName, objectKey, versionId=None)
    函数功能：获取对象的ACL
    参数说明: bucketName：桶名 （必填）
    objectKey：对象名
    versionId：对象版本号
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: ACL对象
    '''

    resp = TestObs.getObjectAcl(bucketName='bucket001', objectKey='test.txt', versionId=None)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body:
        print('owner_id:', resp.body.owner.owner_id, ',owner_name:', resp.body.owner.owner_name)
        i = 0
        for grant in resp.body.grants:
            print('Grant[', i, ']:')
            i += 1
            print('permission:', grant.permission)
            print('grantee_name:', grant.grantee.grantee_name, ',grantee_id:', grant.grantee.grantee_id, ',grantee.group:', grant.grantee.group)

def DeleteObject():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    函数原型： deleteObject(self , bucketName, objectKey, versionId=None)
    函数功能：删除对象
    参数说明: bucketName：桶名 （必填）
    objectKey：对象名
    versionId：对象版本号
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: None
    '''

    resp = TestObs.deleteObject(bucketName='bucket001', objectKey='test.txt', versionId=None)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)

def DeleteObjects():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    from com.obs.models.delete_objects_request import Object,DeleteObjectsRequset
    函数原型： def deleteObjects(self, bucketName, deleteObjectsRequset)
    函数功能：批量删除对象
    参数说明: bucketName：桶名 （必填）
    deleteObjectsRequset：DeleteObjectsRequset 对象 批量删除对象列表请求
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: DeleteObjectsResponse
    '''

    Lobject1 = Object(key='test.xml', versionId=None)
    # Lobject1.key:对象名
    # Lobject1.versionId:对象版本号
    Lobject2 = Object(key='test.txt', versionId=None)
    Lobject3 = Object(key='test', versionId=None)
    Lobjects = [Lobject1, Lobject2, Lobject3]

    Lreq = DeleteObjectsRequest(quiet=False, objects=Lobjects)
    # Lreq.quiet:用于指定使用quiet模式，只返回删除失败的对象结果；如果有此字段，则必被置为True，如果为False则被系统忽略掉。
    # Lreq.objects:待删除的对象列表

    resp = TestObs.deleteObjects(bucketName='bucket001', deleteObjectsRequset=Lreq)
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

def AbortMultipartUpload():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    函数原型：abortMultipartUpload(self , bucketName, objectKey, uploadId)
    函数功能：取消多段上传任务
    参数说明: bucketName：桶名 （必填）
    objectKey:对象名
    uploadId：多段上传任务Id
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: None
   '''

    resp = TestObs.abortMultipartUpload(bucketName='bucket001', objectKey='test.zip', uploadId='0001AB175A0000015C7C5D87ADBD2AP5')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)


def InitiateMultipartUpload():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    函数原型：def initiateMultipartUpload(self, bucketName, objectKey, acl=None, metadata=None, websiteRedirectLocation=None, contentType=None, sseHeader=SseHeader()):
    函数功能: 初始化上传段任务
    参数说明: bucketName：桶名 （必填）
    websiteRedirectLocation:当桶设置了Website配置，可以将获取这个对象的请求重定向到桶内另一个对象或一个外部的URL
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: InitiateMultipartUploadResponse 对象
    '''

    resp = TestObs.initiateMultipartUpload(bucketName='bucket001', objectKey='test.zip', websiteRedirectLocation=None)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body:
        print('bucketName:', resp.body.bucketName, ',objectKey:', resp.body.objectKey, ',uploadId:', resp.body.uploadId)


def CompleteMultipartUpload():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    from com.obs.models.complete_multipart_upload_request import CompletePart,CompleteMultipartUploadRequest
    函数原型：completeMultipartUpload(self , bucketName, objectKey, uploadId, completeMultipartUploadRequest=CompleteMultipartUploadRequest())
    函数功能：取消多段上传任务
    参数说明: bucketName：桶名 （必填）
    objectKey:对象名
    uploadId：多段上传任务Id
    completeMultipartUploadRequest:CompleteMultipartUploadRequest 对象
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: CompleteMultipartUploadResponse 对象
   '''

    Lpart1 = CompletePart(partNum=1, etag='e97f0beed4d87dd49203a21efcb557e6')
    # Lpart1.partNum:段号
    # Lpart1.etag:对应段的ETag值
    Lpart2 = CompletePart(partNum=2, etag='5f8bb5e6ce16ab638d6b7df6942f0904')
    Lparts = []
    Lparts.append(Lpart1)
    Lparts.append(Lpart2)


    LcompleteMultipartUploadRequest = CompleteMultipartUploadRequest(parts=Lparts)
    # LcompleteMultipartUploadRequest.parts:CompletePart对象的链表

    resp = TestObs.completeMultipartUpload(bucketName='bucket001', objectKey='test.zip', uploadId='0001AB175A0000015C7C473EFB962682',
                                           completeMultipartUploadRequest=LcompleteMultipartUploadRequest)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body:
        print('location:', resp.body.location, ',bucket:', resp.body.bucket, ',key:', resp.body.key, ',eTag:', resp.body.eTag)


def UploadPart():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    函数原型：def uploadPart(self, bucketName, objectKey, partNumber, uploadId, object, isFile=False, partSize=None, offset=0, sseHeader=SseHeader(), isAttachMd5 = False):
    函数功能：上传段
    参数说明: bucketName：桶名 （必填）
    objectKey:对象名（必填）
    partNumber：上传段的段号。取值为从1到10000的整数（必填）
    uploadId：多段上传任务Id（必填）
    object：上传文件路径或上传的内容（必填）
    isFile：对象是否为文件（选填）
    partSize: 多段上传任务中某一分段的大小，默认值为文件大小除去offset的剩下字节数，单位字节（选填）
    offset: 多段上传文件任务中某一分段偏移的大小，默认值为0， 单位字节（选填）
    sseHeader    服务端加密头信息，用于加密对象
    isAttachMd5  是否传递MD5值到请求头信息
    返回值：GetResult对象,GetResult.header: 返回头部信息， GetResult.body: None
    '''

    # 假设bigfile.zip有300M，第一次传递100M，第二次传递200M
    resp = TestObs.uploadPart(bucketName='bucket001', objectKey='test.zip', partNumber=1, uploadId='0001AB175A0000015C7C5D87ADBD2AP5',
                              object=r'c:\bigfile.zip', isFile=True, partSize=100 * 1024 * 1024, offset=0)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage), ',header:', resp.header

    resp = TestObs.uploadPart(bucketName='bucket001', objectKey='test.zip', partNumber=2, uploadId='0001AB175A0000015C7C5D87ADBD2AP5',
                              object=r'c:\bigfile.zip', isFile=True, partSize=200 * 1024 * 1024,
                              offset=100 * 1024 * 1024)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage), ',header:', resp.header


def CopyPart():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    函数原型：def copyPart(self, bucketName, objectKey, partNumber, uploadId, copySource, copySourceRange=None, destSseHeader=SseHeader(), sourceSseHeader=SseHeader()):
    函数功能：列出已上传的段
    参数说明: bucketName：桶名 （必填）
    objectKey:对象名
    partNumber:上传段的段号。取值为从1到10000的整数
    uploadId：多段上传任务Id
    copySource：拷贝的源对象
    copySourceRange：源对象中待拷贝的段的字节范围（start - end），start为段起始字节，end为段结束字节
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: CopyPartResponse 对象
    '''

    resp = TestObs.copyPart(bucketName='bucket001', objectKey='test.txt', partNumber=1, uploadId='0001AB175A0000015C7C473EFB962682',
                            copySource='bucket002/test.txt')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body:
        print('modifiedDate:', resp.body.modifiedDate, ',etagValue:', resp.body.etagValue)


def ListParts():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    函数原型：listParts(self, bucketName, objectKey, uploadId, maxParts=None, partNumberMarker=None)
    函数功能：列出已上传的段
    参数说明: bucketName：桶名 （必填）
    objectKey:对象名
    uploadId：多段上传任务Id
    maxParts：规定在列举已上传段响应中的最大Part数目 （默认值：1000）
    partNumberMarker：指定List的起始位置，只有Part Number数目大于该参数的Part会被列出
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: ListPartsResponse 对象
    '''

    resp = TestObs.listParts(bucketName='bucket001', objectKey='test.zip', uploadId='0001AB175A0000015C7C5D87ADBD2AP5', maxParts=None,
                             partNumberMarker=None)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body:
        print('bucketName:', resp.body.bucketName, ',objectKey:', resp.body.objectKey, ',uploadId:', resp.body.uploadId, ',storageClass:', resp.body.storageClass,)
        print('partNumbermarker:', resp.body.partNumbermarker, ',nextPartNumberMarker:', resp.body.nextPartNumberMarker, ',maxParts:', resp.body.maxParts, ',isTruncated:', resp.body.isTruncated,)
        if resp.body.initiator:
            print('initiator.name:', resp.body.initiator.name, ',initiator.id:', resp.body.initiator.id)
        if resp.body.parts:
            i = 0
            for part in resp.body.parts:
                print('part[', i, ']:')
                i += 1
                print('partNumber:', part.partNumber, ',lastModified:', part.lastModified, ',etag:', part.etag, ',size:', part.size)

def RestoreObject():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    函数原型： restoreObject(self, bucketName, objectKey, days, tier=None, versionId=None):
    函数功能：取回归档存储对象
    参数说明: bucketName：桶名 （必填）
    objectKey:对象名(必填)
    days:取回对象的保存时间（单位：天），最小值为1，最大值为30（必填）
    tier:取回选项，支持三种取值：[Expedited|Standard|Bulk]。Expedited表示取回对象耗时1~5分钟，Standard表示耗时3~5小时，Bulk表示耗时5~12小时。默认取值为Standard (选填)
    versionId：待取回冷存储对象的版本号(选填)
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: None
    '''
    resp = TestObs.restoreObject(bucketName='bucket001',objectKey='test.txt', days=1, versionId=None,tier=TierType.EXPEDITED)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)

def GetObjectMetadata():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    函数原型：getObjectMetadata(self, bucketName, objectKey, versionId=None, sseHeader=SseHeader())
    函数功能:下载对象元数据
    参数说明: bucketName：桶名 （必填）
    objectKey:对象名
    versionId：对象版本号
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: None
   '''

    resp = TestObs.getObjectMetadata(bucketName='bucket001', objectKey='test.txt', versionId=None)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    header = dict(resp.header)  # 元组链表转为字典
    print(header.get('etag'))
    print(header.get('x-amz-expiration'))
    print(header.get('x-amz-website-redirect-location'))
    print(header.get('x-amz-version-id'))


def PutObject():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    from com.obs.models.put_object_header import PutObjectHeader
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
    Lheaders = PutObjectHeader(md5=None, acl='private', location=None, contentType='text/plain', sseHeader=sseHeader)
    # Lheaders.md:对象的MD5值
    # Lheaders.acl:可以加上此消息头设置对象的权限控制策略，使用的策略为预定义的常用策略
    # Lheaders.location:当桶设置了Website配置，可以将获取这个对象的请求重定向到桶内另一个对象或一个外部的URL

    Lmetadata = {'key': 'value'}

    resp = TestObs.putObject(bucketName='bucket001', objectKey='test.txt', content='msg content to put',
                             metadata=Lmetadata, headers=Lheaders)

    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    print(resp.header)


def PostObject():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    from com.obs.models.put_object_header import PutObjectHeader
    from com.obs.models.server_side_encryption import SseKmsHeader,SseCHeader
    函数原型：postObject(self, bucketName, objectKey, file_path, metadata=None, headers=None)
    函数功能：上传对象 （上传内容）
    参数说明: bucketName：桶名 （必填）
    objectKey:对象名
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

    Lheaders.sseHeader = SseKmsHeader.getInstance()

    Lmetadata = {'key': 'value'}
    file_path = r'C:\test.txt'

    resp = TestObs.postObject(bucketName='bucket001', objectKey='test.txt', file_path=file_path,
                              metadata=Lmetadata, headers=Lheaders)
    if isinstance(resp, list):
        for k, v in resp:
            print('objectKey',k, 'common msg:status:', v.status, ',errorCode:', v.errorCode, ',errorMessage:', v.errorMessage)
    else:
        print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)


def CopyObject():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    from com.obs.models.copy_object_header import CopyObjectHeader
    from com.obs.models.date_time import DateTime
    函数原型：copyObject(self, sourceBucketName, sourceObjectKey, destBucketName, destObjectKey, metadata=None, headers=CopyObjectHeader(),versionId=None)
    函数功能：上传对象 （上传内容）
    参数说明: sourceBucketName：原桶名 （必填）
    sourceObjectKey:原对象名
    destBucketName：目标桶名
    destObjectKey: 目标对象名
    metadata：加入自定义的元数据，以便对对象进行自定义管理
    headers:附加消息头
    versionId:被复制的对象版本号
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: CopyObjectResponse
   '''
    Lheader = CopyObjectHeader(acl=None, directive=None, if_match=None, if_none_match=None,
                               if_modified_since=DateTime(2017,6,6), if_unmodified_since=None,
                               location=None)
    # Lheader.acl 复制对象时，可以加上此消息头设置对象的权限控制策略，使用的策略为预定义的常用策略，包括：private；public-read；public-read-write；authenticated-read；bucket-owner-read；bucket-owner-full-control。
    # Lheader.directive 此参数用来指定新对象的元数据是从源对象中复制，还是用请求中的元数据替换。有效取值：COPY或REPLACE。
    # Lheader.if_match 如果对象的ETag和请求中指定的ETag相同，则返回对象内容，否则的话返回412（precondition failed）。
    # Lheader.if_none_match 如果对象的ETag和请求中指定的ETag不相同，则返回对象内容，否则的话返回412 (not modified）。
    # Lheader.if_modified_since DateTime对象， 如果对象在请求中指定的时间之后有修改，则返回对象内容；否则的话返回412（not modified）。
    # Lheader.if_unmodified_since DateTime对象 ，如果对象在请求中指定的时间之后没有修改，则返回对象内容；否则的话返回412（precondition failed）。
    # Lheader.location 当桶设置了Website配置，可以将获取这个对象的请求重定向到桶内另一个对象或一个外部的URL，UDS将这个值从头域中取出，保存在对象的元数据中。

    Lmetadata = {'key': 'value'}
    resp = TestObs.copyObject(sourceBucketName='bucket002', sourceObjectKey='test.txt', destBucketName='bucket001',
                              destObjectKey='test.txt', metadata=Lmetadata, headers=Lheader)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body:
        print('lastModified:', resp.body.lastModified, ',eTag:', resp.body.eTag)


def GetObject():
    '''
    引入库: from com.obs.client.obs_client import ObsClient
    from com.obs.models.get_object_request import GetObjectRequest
    from com.obs.models.get_object_header import GetObjectHeader
    函数原型：getObject(self , bucketName, objectKey, downloadPath=None, getObjectRequest=GetObjectRequest(), headers=GetObjectHeader(), loadStreamInMemory=False)
    函数功能:下载对象
    参数说明: bucketName：桶名 （必填）
    objectKey:对象名
    downloadPath：下载到本地的路径
    getObjectRequest: GetObjectRequest对象
    headers:附加消息头
    loadStreamInMemory:  是否将对象流加载到内存
    返回值：GetResult对象,GetResult.header: 返回头部信息 , GetResult.body: ObjectStream对象
   '''

    LobjectRequest = GetObjectRequest(content_type='text/plain', content_language=None, expires=None,
                                      cache_control=None, content_disposition=None, content_encoding=None,
                                      versionId=None)
    # LobjectRequest.content_type： 重写响应中的Content-Type头。
    # LobjectRequest.contecontent_languagent_type：     重写响应中的Content-Language头。
    # LobjectRequest.expires：     重写响应中的Expires头。
    # LobjectRequest.cache_control：     重写响应中的Cache-Control头。
    # LobjectRequest.content_disposition：     重写响应中的Content-Disposition头。
    # LobjectRequest.content_encoding：     重写响应中的Content-Encoding头。
    # LobjectRequest.versionId ：    指定获取对象的版本号。

    Lheaders = GetObjectHeader(range='0-10', if_modified_since=None, if_unmodified_since=None, if_match=None,
                               if_none_match=None)
    # Lheaders.range: 获取对象时获取在Range范围内的对象内容；如果Range不合法则忽略此字段下载整个对象;Range是一个范围，它的起始值最小为0，最大为对象长度减1。
    # Lheaders.if_modified_since: DateTime对象，如果对象在请求中指定的时间之后有修改，则返回对象内容；否则的话返回304（not modified）。
    # Lheaders.if_unmodified_since: DateTime对象，如果对象在请求中指定的时间之后没有修改，则返回对象内容；否则的话返回412（precondition failed）。
    # Lheaders.if_match: 如果对象的ETag和请求中指定的ETag相同，则返回对象内容，否则的话返回412（precondition failed）。
    # Lheaders.if_none_match: 如果对象的ETag和请求中指定的ETag不相同，则返回对象内容，否则的话返回304（not modified）。

    loadStreamInMemory = True
    resp = TestObs.getObject(bucketName='bucket001', objectKey='test.txt', downloadPath=r'C:\test',
                             getObjectRequest=LobjectRequest, headers=Lheaders, loadStreamInMemory=loadStreamInMemory)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage, ',header:' , resp.header)
    if isinstance(resp.body, ObjectStream):
        if loadStreamInMemory:
            print(resp.body.buffer)
            print(resp.body.size)
        else:
            response = resp.body.response
            chunk_size = 65536
            if response is not None:
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    print(chunk)
                response.close()
    else:
        print(resp.body)

if __name__ == '__main__':
    # initLog()
    #=========================================================
    # 桶操作
    # =========================================================
    # CreateBucket()
    # DeleteBucket()
    # ListBuckets()
    # HeadBucket()
    # GetBucketMetadata()
    # SetBucketQuota()
    # GetBucketQuota()
    # GetBucketStorageInfo()
    # SetBucketAcl()
    # GetBucketAcl()
    # SetBucketPolicy()
    # GetBucketPolicy()
    # DeleteBucketPolicy()
    # SetBucketVersioningConfiguration()
    # GetBucketVersioningConfiguration()
    # ListVersions()
    # ListObjects()
    # ListMultipartUploads()
    # DeleteBucketLifecycleConfiguration()
    # SetBucketLifecycleConfiguration()
    # GetBucketLifecycleConfiguration()
    # DeleteBucketWebsiteConfiguration()
    # SetBucketWebsiteConfiguration()
    # GetBucketWebsiteConfiguration()
    # SetBucketLoggingConfiguration()
    # GetBucketLoggingConfiguration()
    # GetBucketLocation()
    # DeleteBucketTagging()
    # SetBucketTagging()
    # GetBucketTagging()
    # DeleteBucketCors()
    # SetBucketCors()
    # GetBucketCors()
    # OptionsBucket()
    # SetBucketNotification()
    # GetBucketNotification()
    #=========================================================
    # 对象操作
    # =========================================================
    # OptionsObject()
    # SetObjectAcl()
    # GetObjectAcl()
    # DeleteObject()
    # DeleteObjects()
    # RestoreObject()
    # AbortMultipartUpload()
    # InitiateMultipartUpload()
    # UploadPart()
    # CompleteMultipartUpload()
    # CopyPart()
    # ListParts()
    # GetObjectMetadata()
    # PutObject()
    # CopyObject()
    # PostObject()
    # GetObject()
    pass
















