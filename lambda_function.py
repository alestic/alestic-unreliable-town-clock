#!/usr/bin/env python3.6
import os
import json
from datetime import datetime
import boto3
import logging

days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def chime(sns_topic_arn, region, event_time, uuid, reference, support):
    chime_time = datetime.strptime(event_time, '%Y-%m-%dT%H:%M:%SZ')
    chime_yyyy = str(chime_time.year)
    chime_mm   = str(chime_time.month).zfill(2)
    chime_dd   = str(chime_time.day).zfill(2)
    chime_hh   = str(chime_time.hour).zfill(2)
    chime_mi   = str(chime_time.minute).zfill(2)
    chime_ss   = str(chime_time.second).zfill(2)
    chime_day  = days[chime_time.weekday()]
    timestamp  = (chime_yyyy + '-' + chime_mm + '-' + chime_dd +
                 ' ' + chime_hh + ':' + chime_mi + ' UTC')
    subject    = "[Unreliable Town Clock] chime: " + timestamp
    message = {
      'source': 'townclock.chime',
      'type': 'chime',
      'version': '3.0',
      'timestamp': timestamp,
      'year': chime_yyyy,
      'month': chime_mm,
      'day': chime_dd,
      'hour': chime_hh,
      'minute': chime_mi,
      'day_of_week': chime_day,
      'unique_id': uuid,
      'region': region,
      'sns_topic_arn': sns_topic_arn,
      'reference': reference,
      'support': support,
      'disclaimer': 'UNRELIABLE SERVICE'
    }
    message_payload = json.dumps(message, indent=2)
    logger.info('message: {}'.format(message_payload))

    client = boto3.client('sns')
    response = client.publish(
        TargetArn=sns_topic_arn,
        Subject=subject,
        MessageStructure='string',
        Message=message_payload
    )
    logger.info('sns publish response: {}'.format(json.dumps(response), indent=2))

def lambda_handler(event, context):
    logger.info('event: {}'.format(json.dumps(event)))
    chime(os.environ['sns_topic_arn'],
          event['region'],
          event['time'],
          event['id'],
          os.environ['reference'],
          os.environ['support']
    )

if __name__ == "__main__":
    os.environ['sns_topic_arn'] = 'arn:aws:sns:us-east-1:522480313337:townclock-TEST-20151008a'
    os.environ['support'] = 'YourNameHere <youremail@example.com>'
    os.environ['reference'] = 'http://townclock.io'
    lambda_handler({
        "version": "0",
        "id": "d9bdd3a1-0fa5-499c-9eb7-e0097e03b54b",
        "detail-type": "Scheduled Event",
        "source": "aws.events",
        "account": "123456789012",
        "time": "2017-05-13T05:15:00Z",
        "region": "us-east-1",
        "resources": [
            "arn:aws:events:us-east-1:123456789012:rule/my-scheduled-rule"
        ],
        "detail": {}
    }, None)
