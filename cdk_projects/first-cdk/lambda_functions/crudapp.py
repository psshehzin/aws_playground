import os
import boto3
import json

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb')

# Retrieve the DynamoDB table name from environment variable
TABLE_NAME = os.environ['TABLE_NAME']

def handler(event, context):
    # Extract the HTTP method from the event
    http_method = event['httpMethod']
    
    # Ensure that the HTTP method is either GET or POST
    if http_method not in ['GET', 'POST']:
        return {
            'statusCode': 405,  # Method Not Allowed
            'body': 'Invalid HTTP method'
        }
    
    # Handle GET request
    if http_method == 'GET':
        # Extract the item_id from the query parameters
        params = event['queryStringParameters']
        item_id = params['item_id']
        try:
            # Retrieve the DynamoDB table
            table = dynamodb.Table(TABLE_NAME)
            
            # Get item from DynamoDB
            response = table.get_item(
                Key={
                    'id': item_id
                }
            )
            
            # Check if the item exists
            if 'Item' in response:
                # Item found, return the item
                item = response['Item']
                return {
                    'statusCode': 200,
                    'body': json.dumps(item)
                }
            else:
                # Item not found
                return {
                    'statusCode': 404,
                    'body': 'Item not found'
                }
        except Exception as e:
            # Error occurred while accessing DynamoDB
            return {
                'statusCode': 500,
                'body': str(e)
            }
    # Handle POST request
    elif http_method == 'POST':
        # Extract the item_id and new_data from the request body
        body = json.loads(event['body'])
        item_id = body['item_id']
        new_data = body['new_data']
        
        try:
            # Retrieve the DynamoDB table
            table = dynamodb.Table(TABLE_NAME)
            
            # Update item in DynamoDB
            table.update_item(
                Key={
                    'id': item_id
                },
                UpdateExpression='SET data = :data',
                ExpressionAttributeValues={
                    ':data': new_data
                }
            )
            
            return {
                'statusCode': 200,
                'body': 'Item updated successfully'
            }
        except Exception as e:
            # Error occurred while updating item in DynamoDB
            return {
                'statusCode': 500,
                'body': str(e)
            }