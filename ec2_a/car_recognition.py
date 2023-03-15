import boto3
import os
from dotenv import load_dotenv

# Import environment variables
load_dotenv('../.env.template')  # Grab from root
bucket_name = os.getenv('BUCKET_NAME')
queue_name = os.getenv('QUEUE_NAME')

# Create rekognition client
rekognition = boto3.client('rekognition', region_name='us-east-1') # Global Region

# Create S3 connection to cs442-unr
s3 = boto3.resource('s3')
bucket = s3.Bucket(bucket_name)

# Create SQS connection to car queue
sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName=queue_name)

# Loop through all images
for img in bucket.objects.all():
    # Label Detection using AWS Rekognition
    ## https://docs.aws.amazon.com/rekognition/latest/APIReference/API_DetectLabels.html
    ## https://github.com/awsdocs/aws-doc-sdk-examples/blob/main/python/example_code/rekognition/rekognition_image_detection.py
    ## https://docs.aws.amazon.com/code-library/latest/ug/python_3_rekognition_code_examples.html
    ## https://docs.aws.amazon.com/rekognition/latest/dg/labels-detect-labels-image.html
    response = rekognition.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucket_name,
                'Name': img.key
            }
        }
    )

    # Checks if car detected with confidence > 90
    for label in response['Labels']:
        if label['Name'] == 'Car' and label['Confidence'] > 90:
            queue.send_message(MessageBody=img.key)  # Send image to queue

queue.send_message(MessageBody="-1")    # Send end of images