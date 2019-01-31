import json
import boto3
import zipfile
import mimetypes
from botocore.client import Config
import StringIO #python2
#from io import StringIO (python3)
def lambda_handler(event, context):

    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-1:902258414832:deployPortfolioTopic')

    try:
        s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))  #without signature_version, the index.html will be downloaded instead of being openned

        yingying3 = s3.Bucket('yingying3')
        yingying2=s3.Bucket('yingying2')


        autoDeployS3website_zip = StringIO.StringIO()
        yingying2.download_fileobj('autoDeployS3website.zip',autoDeployS3website_zip)

        #yingying2.download_file('autoDeployS3website.zip','c:/Users/wenyi/autoDeployS3website.zip')



        #with zipfile.ZipFile('c:/Users/wenyi/autoDeployS3website.zip') as myzip:
        #    for nm in myzip.namelist():
        #        print(nm)

        with zipfile.ZipFile(autoDeployS3website_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                yingying3.upload_fileobj(obj,nm,
                    ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
                yingying3.Object(nm).Acl().put(ACL='public-read') #S3 need to be public accessible, but not necessary be ALL PUBLIC

        topic.publish(Subject="Portfolio deployed", Message="Portfolio deployed successfully!")
    except:
        topic.publish(Subject="Portfolio deploy Failed", Message="Portfolio was not deployed successfully!")
        raise
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')

    }
