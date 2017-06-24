# AWS Codepipeline To S3
An AWS Lambda function that leverages Codepipeline to update an S3 bucket when code is pushed to a Git repository.

AWS allows you to use an S3 bucket to serve static websites. The tutorial can be found here: http://docs.aws.amazon.com/AmazonS3/latest/dev/hosting-websites-on-s3-examples.html

This Lambda function leverages AWS Codepipeline to update the static content in S3 for the website when a code update is pushed to Git. 

This will work with either GitHub or AWS Codecommit as the Git repository.

## Why not a trigger instead?

Both AWS Codecommit and GitHub support 'triggers'. When certain actions such as a push to a branch are done, external webservices can be invoked. In theory you could use a trigger coupled with associated services to update your S3 bucket instead of Codepipeline. However, you would still need to use Lambda. Instead of using AWS Codepipeline, you would use the AWS API Gateway service. The Git trigger would call the API Gateway which would then trigger an AWS Lambda function. 

In this scenario the Lambda function would


First step to CI

## Setup

### Prerequisites

The following will need to be setup before you can use this Lambda function to update your S3 static website:

* An AWS Codecommit or GitHub repository 
* A static hosted website in S3 

### Setup Codepipeline
