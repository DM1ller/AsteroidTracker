import json
import boto3

def lambda_handler(event, context):
    data = get_data_dynamodb()
    response = {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            
        },
        'body': json.dumps(data)
    }
    return response
    
    
    
def get_data_dynamodb():    
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.scan(TableName='Asteroids_DynamoDB')
    return response['Items']