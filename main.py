import os
import json
import boto3
from dotenv import load_dotenv

load_dotenv()

region = os.getenv('AWS_REGION',None)
sqs_client = boto3.client('sqs', region_name=region)

SQS_URL = os.getenv('SQS_URL',None)
AWS_ACOUNT_ID = os.getenv('AWS_ACOUNT_ID',None)
QUEUE_NAME = os.getenv('QUEUE_NAME',None)

if __name__ == '__main__':

  # キューURLの取得
  queue_url = '{0}/{1}/{2}'.format(SQS_URL,AWS_ACOUNT_ID,QUEUE_NAME)

  # キューメッセージの取得
  response = sqs_client.receive_message(
    QueueUrl=queue_url,
    AttributeNames=[
    'SentTimestamp'
    ],
    MaxNumberOfMessages=1,
    VisibilityTimeout=10,
    WaitTimeSeconds=10
  )

  # キューメッセージの表示・削除
  if len(response['Messages']):
    message = response['Messages'][0]
    
    if 'Body' in message and 'ReceiptHandle' in message:
      print(message['Body'])
      receipt_handle = message['ReceiptHandle']
      sqs_client.delete_message(QueueUrl=queue_url,ReceiptHandle=receipt_handle)

  else:
    print('None Queue')    

