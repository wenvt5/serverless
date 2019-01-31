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

    location = {
        "bucketName": 'yingying2',
        "objectKey":'autoDeployS3website.zip'
    }
    try:
        job = event.get("CodePipeline.job")

        # if job initiated by pipeline, a new bucket and path is created by aws, unless you configure the artifact setting in console
        # in this case, I have configure artifact setting so that in case of the pipeline, the artifact will still be saved in the same bucket, same path and same file name
        if job:
            for artifact in job["data"]["inputArtifacts"]:
                if artifact["name"] == "MyAppBuild":
                    location = artifact["location"]["s3Location"]

        print "Building portfolio from " + str(location)

        s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))  #without signature_version, the index.html will be downloaded instead of being openned

        yingying3 = s3.Bucket('yingying3')
        yingying2=s3.Bucket(location['bucketName'])


        autoDeployS3website_zip = StringIO.StringIO()
        yingying2.download_fileobj(location['objectKey'],autoDeployS3website_zip)

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

        # if job initiated by pipeline, lambda need to tell pipeline that the job is done and next step need to be initiated
        if job:
            codepipeline = boto3.client('codepipeline')
            codepipeline.put_job_success_result(jobId=job["id"])
    except:
        topic.publish(Subject="Portfolio deploy Failed", Message="Portfolio was not deployed successfully!")
        raise
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')

    }
