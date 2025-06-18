import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PortfolioVisitorCount')

def lambda_handler(event, context):
    response = table.update_item(
        Key={'id': 'visitorCount'},
        UpdateExpression='SET #c = if_not_exists(#c, :start) + :inc',
        ExpressionAttributeNames={'#c': 'count'},
        ExpressionAttributeValues={':inc': 1, ':start': 0},
        ReturnValues='UPDATED_NEW'
    )
    new_count = response['Attributes']['count']
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
        'body': json.dumps({'visitorCount': int(new_count)})
    }
