import json
import boto3
import os
import random
import string
from urllib.parse import urlparse

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME', 'ShortLinks')
table = dynamodb.Table(table_name)

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def lambda_handler(event, context):
    print("Incoming event:", json.dumps(event))
    
    try:
        body = json.loads(event.get('body', '{}'))
        original_url = body.get('url')
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid request format'})
        }

    if not original_url or not is_valid_url(original_url):
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid or missing URL'})
        }

    short_code = generate_short_code()

    try:
        table.put_item(Item={
            'shortCode': short_code,
            'originalUrl': original_url
        })
    except Exception as e:
        print("DynamoDB PutItem error:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Failed to store short link'})
        }

    base_url = os.environ.get('BASE_URL', 'https://your-api-id.execute-api.us-east-1.amazonaws.com')
    short_url = f"{base_url}/{short_code}"

    return {
        'statusCode': 200,
        'body': json.dumps({
            'shortCode': short_code,
            'shortUrl': short_url
        })
    }
