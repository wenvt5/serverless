import boto3
import zipfile
import mimetypes

s3 = boto3.resource('s3')

yingying3 = s3.Bucket('yingying3')
yingying2=s3.Bucket('yingying2')

#from io import StringIO
#autoDeployS3website_zip = StringIO()
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
        yingying3.Object(nm).Acl().put(ACL='public-read')
