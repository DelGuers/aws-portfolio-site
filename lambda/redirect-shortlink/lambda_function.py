import json
import boto3
import os

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME', 'ShortLinks')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    print("Incoming event:", json.dumps(event))
    
    short_code = event.get('rawPath', '/').lstrip('/')
    print("Short code extracted:", short_code)

    # Handle root path with no short code
    if not short_code:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing short code in path'})
        }

    try:
        response = table.get_item(Key={'shortCode': short_code})
        print("DynamoDB response:", response)
    except Exception as e:
        print("Error querying DynamoDB:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal Server Error'}),
        }

    item = response.get('Item')

    if not item:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Short link not found'}),
        }

    # Redirect to the original URL
    return {
        'statusCode': 301,
        'headers': {
            'Location': item['originalUrl']
        },
        'body': ''
    }
