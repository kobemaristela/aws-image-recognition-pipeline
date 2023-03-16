# Cloud Computing - Project Assignment 1

The purpose of this individual assignment is to learn how to use the Amazon AWS cloud platform and how to develop an AWS application that uses existing cloud services. You Will be building an image recognition pipeline in AWS, using two EC2 instances, S3, SQS, and Rekognition.

This guide will walk you through deploying a CloudFormation stack that satisfies all the requirements for the project.

## Prerequisites

- Key pair created in AWS
- AWS CLI installed and configured (optional)


## Deployment Steps

### AWS Console
1. Navigate to AWS CloudFormation
2. Click on 'Create Stack'
3. Upload the 'cloud_deploy.yaml' template file
4. Enter a 'Stack Name'
5. Click 'Next' until you on the last screen (feel free to change the defaults)
6. Click Submit (and wait for your instances to be deployed approx. 3-5 mins)

### AWS CLI (optional)
1. Clone this repository to your local machine.
2. Navigate inside the cloned repository
3. Deploy the cloudformation template
```bash
  aws cloudformation deploy --template-file cloud_deploy.yaml --stack-name your-stack-name
```

## Usage
1. SSH into each respective EC2 instances
2. Navigate into the 'aws-image-recognition-pipeline' directory
3. Navigate into each respective ec2 directories (ec2_a | ec2_b)
4. Run the respective python program for each instance (car_recognition.py | text_recognition.py)

## Cleanup
### AWS Console
1. Navigate to AWS CloudFormation
2. Click on 'Delete Stack' for your stack

### AWS CLI
```bash
  aws cloudformation delete-stack --stack-name your-stack-name
```
