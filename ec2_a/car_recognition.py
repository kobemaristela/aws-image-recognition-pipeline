import os
import boto3
from dotenv import load_dotenv

# Import environment variables
load_dotenv('../.env.template')  # Grab from root
bucket_name = os.getenv('BUCKET_NAME')
queue_name = os.getenv('QUEUE_NAME')
region_name = os.getenv('REGION_NAME')

# Initiate rekognition client
rekognition = boto3.client('rekognition', region_name=region_name)  # IMPORTANT - Global Region

# Initiate S3 connection to bucket
s3 = boto3.resource('s3')
bucket = s3.Bucket(bucket_name)

# Initiate SQS connection to car queue
sqs = boto3.resource('sqs', region_name=region_name)
queue = sqs.get_queue_by_name(QueueName=queue_name)

# Loop through all images
for image in bucket.objects.all():
    # Label Detection using AWS Rekognition
    ## https://docs.aws.amazon.com/rekognition/latest/APIReference/API_DetectLabels.html
    ## https://github.com/awsdocs/aws-doc-sdk-examples/blob/main/python/example_code/rekognition/rekognition_image_detection.py
    ## https://docs.aws.amazon.com/code-library/latest/ug/python_3_rekognition_code_examples.html
    ## https://docs.aws.amazon.com/rekognition/latest/dg/labels-detect-labels-image.html
    response = rekognition.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucket_name,
                'Name': image.key
            }
        }
    )

    # Checks if car detected with confidence > 90
    for label in response['Labels']:
        if label['Name'] == 'Car' and label['Confidence'] >= 90:
            print(f'Car Image Found: {image.key}')
            queue.send_message(MessageBody=image.key, MessageGroupId="car-recognition")  # Send image to queue

queue.send_message(MessageBody="-1", MessageGroupId="car-recognition")    # Send end of images
print("Car Detection Complete...")

