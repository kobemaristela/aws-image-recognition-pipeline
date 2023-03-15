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

while True:
    # Read incoming message from SQS
    messages = queue.receive_messages()

    for message in messages:
        image = message.body
        print(f"Processing image: {image}")

        # Termination index detected - break out of loop
        if image == "-1":
            message.delete()    # Delete terminate message
            print("Text Recognition Complete...")
            break

        # Text Detection using AWS Rekognition
        ## https://docs.aws.amazon.com/code-library/latest/ug/python_3_rekognition_code_examples.html
        ## https://docs.aws.amazon.com/rekognition/latest/APIReference/API_DetectText.html
        ## https://docs.aws.amazon.com/rekognition/latest/dg/text-detecting-text-procedure.html
        response = rekognition.detect_text(
            Image={
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': image
                }
            }
        )

        # Check if the image contains any text
        if len(response['TextDetections']) > 0:
            # Compile all detected text
            text_found = ""
            for detected_text in response['TextDetections']:
                if detected_text['Type'] == 'LINE':
                    text_found += detected_text['DetectedText'] + ", "

            # Write text detected to outfile
            with open('output.txt', 'a') as f:
                f.write(f"{image}: {text_found}\n")

        # Remove message
        message.delete()
