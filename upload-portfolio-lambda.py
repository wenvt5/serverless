import boto3
import zipfile
import mimetypes
from botocore.client import Config
s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))  #without signature_version, the index.html will be downloaded instead of being openned

yingying3 = s3.Bucket('yingying3')
yingying2=s3.Bucket('yingying2')

#from io import StringIO (python3)
# the following commented lines are only for python2
#import StringIO
#autoDeployS3website_zip = StringIO.StringIO()
#yingying2.download_fileobj('autoDeployS3website.zip',autoDeployS3website_zip)

yingying2.download_file('autoDeployS3website.zip','c:/Users/wenyi/autoDeployS3website.zip')



with zipfile.ZipFile('c:/Users/wenyi/autoDeployS3website.zip') as myzip:
    for nm in myzip.namelist():
        print(nm)

with zipfile.ZipFile('c:/Users/wenyi/autoDeployS3website.zip') as myzip:
    for nm in myzip.namelist():
        obj = myzip.open(nm)
        yingying3.upload_fileobj(obj,nm,
            ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
        yingying3.Object(nm).Acl().put(ACL='public-read') #S3 need to be public accessible, but not necessary be ALL PUBLIC
