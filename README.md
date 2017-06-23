# AWS Codepipeline To S3
An AWS Lambda function that leverages Codepipeline to update an S3 bucket when code is pushed to a Git repository.

AWS allows you to use an S3 bucket to serve static websites. The tutorial can be found here: http://docs.aws.amazon.com/AmazonS3/latest/dev/hosting-websites-on-s3-examples.html

This Lambda function leverages AWS Codepipeline to update the static content in S3 for the website when a code update is pushed to Git. 

This will work with either GitHub or AWS Codecommit as the Git repository.

## Why not a trigger instead?

Two services either way

First step to CI

## Setup Codepipeline 