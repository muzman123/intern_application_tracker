import boto3
from botocore.exceptions import ClientError

def saveToDynamoTable(from_address, subject, body, table_name="RejectionEmails"):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    
    try:
        response = table.put_item(
            Item={
                'EmailID': from_address,
                'Subject': subject,
                'Body': body
            }
        )
        return response
    except ClientError as e:
        print(f"Error saving to DynamoDB: {e.response['Error']['Message']}")