import boto3
import botocore
import zipfile
import tempfile

def setup_s3_client(job_data):
    """
    Creates an S3 client

    Uses the credentials passed in the event by CodePipeline. These
    credentials can be used to access the artifact bucket.

    Args:
        job_data: The job data structure

    Returns:
        An S3 client with the appropriate credentials

    """
    key_id = job_data['artifactCredentials']['accessKeyId']
    key_secret = job_data['artifactCredentials']['secretAccessKey']
    session_token = job_data['artifactCredentials']['sessionToken']

    session = boto3.session.Session(aws_access_key_id=key_id,
        aws_secret_access_key=key_secret,
        aws_session_token=session_token)
    return session.client('s3', config=botocore.client.Config(signature_version='s3v4'))

def lambda_handler(event, context):
    jobid = event['CodePipeline.job']['id']
    jobdata = event['CodePipeline.job']['data']
    inputartifact = event['CodePipeline.job']['data']['inputArtifacts'][0]
    location = inputartifact['location']['s3Location']
    bucketname = location['bucketName']
    objectkey = location['objectKey']
    objectname = inputartifact['name']

    print (bucketname)
    print (objectkey)
    print (objectname)

    tempzipfile = tempfile.NamedTemporaryFile(delete=False)
    print (tempzipfile.name)
    tempzipfile.close()

    s3 = setup_s3_client(jobdata)
    s3.download_file(bucketname, objectkey, tempzipfile.name)

    archive = zipfile.ZipFile(tempzipfile.name)
    uploads3 = boto3.client('s3')
    for archivefile in archive.namelist():
        print (archivefile)
        with archive.open(archivefile) as data:
            uploads3.upload_fileobj(data, 'mattp.it', archivefile)

    lambdaClient = boto3.client('codepipeline')
    lambdaClient.put_job_success_result(jobId=jobid)

    return