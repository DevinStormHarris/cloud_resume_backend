import boto3
import json

# initialize boto3 resources
dynamo = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamo.Table('VisitorCount')

def lambda_handler(event, context):

    try:
        # get current value from ddb
        print ("[INFO] Retrieving current count from table")
        resp = table.get_item(Key={'Count': 1})
        print(resp)
        current = resp['Item']['VisitorCount']
        print(current)


        # add 1
        current += 1
        print(current)
        
        # update ddb
        print ("[INFO] Updating table with count")
        table.update_item(
            Key={'Count': 1},
            UpdateExpression='SET VisitorCount=:val1',
            ExpressionAttributeValues={':val1': current}
        )
        print ("[INFO] Retrieved count, returning to client")
        # return to website
        return {
            'body': json.dumps({
                'count': str(current), }),
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'application/json',
                'Access-Control-Allow-Methods': 'OPTIONS,POST',
                'Access-Control-Allow-Credentials': 'true'
            },
        }

    except Exception as e:
        print ("[ERROR] Unexpected error, check logs")
        return {
            'statusCode': 500,
            'error': str(e)
        }