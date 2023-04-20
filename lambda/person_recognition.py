import boto3

# Initiate sqs & rekognition client
rekognition = boto3.client('rekognition', region_name='us-east-1')  # IMPORTANT - Global Region

# Initiate SQS connection to car queue
sqs = boto3.resource('sqs', region_name='us-east-1')
queue = sqs.get_queue_by_name(QueueName='person-recognition-queue.fifo')

# https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html
def lambda_handler(event, context):
    for message in event['Records']:
        # Read incoming message from event trigger
        image = message['body']

        # Termination index detected - End of Detection
        if image == "-1":
            print("Person Detection Complete...")
            queue.send_message(MessageBody="-1", MessageGroupId="person-recognition")
            return {'statusCode': 200, 'body': 'Person Detection Complete...'}

        # Label Detection using AWS Rekognition
        response = rekognition.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': 'cs442-unr',
                    'Name': image
                }
            }
        )

        # Checks if car detected with confidence > 90
        for label in response['Labels']:
            if label['Name'] == 'Person' and label['Confidence'] > 90:
                print(f'Person Image Found: {image}')
                queue.send_message(MessageBody=image, MessageGroupId="person-recognition")
                return {'statusCode': 200, 'body': f'Person Image Found: {image}'}
