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
    """
    lambda_handler is the entry point that is invoked when the lambda function is called,
    more information can be found in the docs: http://docs.aws.amazon.com/lambda/latest/dg/python-programming-model-handler-types.html

    Get the input artifact zip from S3, download to a temp file, extract the individual files and upload them to
    the S3 bucket that hosts the static files for the site.
    """

    # Get the required variables from the event object
    jobid = event['CodePipeline.job']['id']
    jobdata = event['CodePipeline.job']['data']
    inputartifact = event['CodePipeline.job']['data']['inputArtifacts'][0]
    location = inputartifact['location']['s3Location']
    bucketname = location['bucketName']
    objectkey = location['objectKey']
    statics3 = 'mattp.it'  # TODO: make this an environment variable

    # Create a temp file to store the artifact zip of the site code to.
    # Each Lambda function has 500MB of temp file storage available to it.
    tempzipfile = tempfile.NamedTemporaryFile(delete=False)
    tempzipfile.close()

    # Download the input artifact zip file containing the site code from the Git repository.
    # The artifact S3 bucket uses SSE so we need a more complicated client setup to access it.
    s3 = setup_s3_client(jobdata)
    s3.download_file(bucketname, objectkey, tempzipfile.name)

    # TODO: make this it's own method.
    archive = zipfile.ZipFile(tempzipfile.name)
    uploads3 = boto3.client('s3')
    for archivefile in archive.namelist():
        with archive.open(archivefile) as data:
            uploads3.upload_fileobj(data, statics3, archivefile)

    # Return success result of the operation to the Codepipeline instance
    # This needs to be done explicitly.
    lambdaClient = boto3.client('codepipeline')
    lambdaClient.put_job_success_result(jobId=jobid)

    return
