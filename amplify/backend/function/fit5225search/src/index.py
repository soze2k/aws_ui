import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

def handler(event, context):
    DB = boto3.resource('dynamodb')
    table = DB.Table('Image')
    print('received event:')
    print(event)
    search_tags = []
    if event['queryStringParameters'] is not None:
        search_tags = list(event['queryStringParameters'].values())

    links = []
    response = table.scan(
        FilterExpression = Attr('id').gte('0')
    )

    if 'Items' in response:
        for x in response['Items']:
            tag_list = x['tags']
            if all(word in tag_list for word in search_tags):
                links.append(x['s3-url'])
    print(links)

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps('Hello from your new Amplify Python lambda!')
    }
